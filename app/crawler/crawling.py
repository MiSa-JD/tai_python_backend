from httpx import AsyncClient
import httpx
import asyncio
from bs4 import BeautifulSoup


async def get_keyword_news(keyword):
    href_links = []
    # 크롤링 할 기사의 개수를 조정합니다.
    limit_cnt = 10

    origin_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"
    async with AsyncClient() as client:
        response = await client.get(url=origin_url, timeout=httpx.Timeout(120.0))
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


async def get_news_from_naver(keyword, urls):
    results = []
    title = ""
    content = ""
    for url in urls:
        async with AsyncClient() as client:
            response = await client.get(url=url, timeout=httpx.Timeout(120.0))
        soup = BeautifulSoup(response.content, "html.parser")

        if "entertain.naver.com" in url:
            title_tag = soup.find("div", class_="ArticleHead_article_head_title__YUNFf")
            content_tag = soup.find("div", class_="_article_content")
            if title_tag is None:
                title = "뉴스의 상태가 잘못되었습니다."
            else:
                title = title_tag.get_text(strip=True)

            if content_tag is None:
                content = "뉴스의 상태가 잘못되었습니다."
            else:
                content = content_tag.get_text(strip=True)

        elif "n.news.naver.com" in url:
            title_tag = soup.find("div", class_="media_end_head_title")
            content_tag = soup.find("div", class_="newsct_article")
            if title_tag is None:
                title = "뉴스의 상태가 잘못되었습니다."
            else:
                title = title_tag.find("span").get_text(strip=True)

            if content_tag is None:
                content = "뉴스의 상태가 잘못되었습니다."
            else:
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
        await asyncio.sleep(0.2)
    return results


async def news_crawling(keyword):
    href_links = await get_keyword_news(keyword)
    news_results = await get_news_from_naver(keyword, href_links)
    return news_results


print("=== Crawler Ready ===")
