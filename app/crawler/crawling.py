import requests
from bs4 import BeautifulSoup
import time


def get_keyword_news(keyword):
    href_links = []
    # 크롤링 할 기사의 개수를 조정합니다.
    limit_cnt = 10

    origin_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"

    response = requests.get(origin_url)
    soup = BeautifulSoup(response.content, "html.parser")

    naver_spans = soup.find_all("span", string="네이버뉴스")

    for news in naver_spans:
        anchor_tag = news.find("a")
        if anchor_tag:
            href = anchor_tag.get("href")
            href_links.append(href)

        if len(href_links) >= limit_cnt:
            break

    return href_links


def get_news_from_naver(keyword, urls):
    results = []
    title = ""
    content = ""
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        if "entertain.naver.com" in url:
            title_tag = soup.find("div", class_="ArticleHead_article_head_title__YUNFf")
            content_tag = soup.find("div", class_="_article_content")
            title = title_tag.get_text(strip=True)
            content = content_tag.get_text(strip=True)

        elif "n.news.naver.com" in url:
            title_tag = soup.find("div", class_="media_end_head_title")
            content_tag = soup.find("div", class_="newsct_article")
            title = title_tag.find("span").get_text(strip=True)
            content = content_tag.get_text(strip=True)
        elif "m.sports.naver.com" in url:
            title_tag = soup.find("h2", class_="ArticleHead_article_title__qh8GV")
            content_tag = soup.find(
                "div", class_="ArticleContent_comp_article_content__luOFM"
            )
            if title_tag is None:
                title = "뉴스의 상태가 잘못되었습니다."
            else:
                title = title_tag.get_text(strip=True)

            if content_tag is None:
                content = "뉴스의 상태가 잘못되었습니다."
            else:
                content = content_tag.get_text(strip=True)

        else:
            print("Unsupported URL format:", url)

        results.append(
            {"keyword": keyword, "link": url, "title": title, "content": content}
        )
        time.sleep(0.2)
    return results


def news_crawling(keyword):
    href_links = get_keyword_news(keyword)
    news_results = get_news_from_naver(keyword, href_links)
    return news_results


print("=== Crawler Ready ===")
