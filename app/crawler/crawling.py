import asyncio
from typing import Optional

import httpx
from bs4 import BeautifulSoup
from httpx import AsyncClient

DEFAULT_ERROR_MESSAGE = "뉴스의 상태가 잘못되었습니다."
REQUEST_TIMEOUT = httpx.Timeout(120.0)
NAVER_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/130.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://m.naver.com/",
}


def _create_client() -> AsyncClient:
    """Create a HTTP client configured for Naver crawling."""
    return AsyncClient(
        headers=NAVER_HEADERS,
        follow_redirects=True,
        timeout=REQUEST_TIMEOUT,
    )


def _safe_text(node, fallback: Optional[str] = None) -> str:
    """Extract text from a BeautifulSoup node or fallback to provided text."""
    if node:
        if hasattr(node, "get_text"):
            return node.get_text(strip=True)
        return str(node).strip()
    if fallback:
        return fallback.strip()
    return DEFAULT_ERROR_MESSAGE


def _get_meta_content(soup: BeautifulSoup, prop: str) -> Optional[str]:
    tag = soup.find("meta", property=prop)
    if tag and tag.get("content"):
        return tag["content"]
    return None


def _parse_entertain_article(soup: BeautifulSoup) -> tuple[str, str]:
    title_tag = soup.find("div", class_="ArticleHead_article_head_title__YUNFf")
    content_tag = soup.find("div", class_="_article_content")
    return (
        _safe_text(title_tag, fallback=_get_meta_content(soup, "og:title")),
        _safe_text(content_tag, fallback=_get_meta_content(soup, "og:description")),
    )


def _parse_news_article(soup: BeautifulSoup) -> tuple[str, str]:
    title_wrapper = soup.find("div", class_="media_end_head_title")
    title_tag = title_wrapper.find("span") if title_wrapper else None
    content_tag = soup.find("div", class_="newsct_article")
    return (
        _safe_text(title_tag, fallback=_get_meta_content(soup, "og:title")),
        _safe_text(content_tag, fallback=_get_meta_content(soup, "og:description")),
    )


def _parse_sports_article(soup: BeautifulSoup) -> tuple[str, str]:
    title_tag = soup.find("h2", class_="ArticleHead_article_title__qh8GV")
    content_tag = soup.find(
        "div", class_="ArticleContent_comp_article_content__luOFM"
    )
    return (
        _safe_text(title_tag, fallback=_get_meta_content(soup, "og:title")),
        _safe_text(content_tag, fallback=_get_meta_content(soup, "og:description")),
    )


def _parse_article(url: str, soup: BeautifulSoup) -> tuple[str, str]:
    if "entertain.naver.com" in url:
        return _parse_entertain_article(soup)
    if "n.news.naver.com" in url:
        return _parse_news_article(soup)
    if "m.sports.naver.com" in url:
        return _parse_sports_article(soup)

    print("Unsupported URL format:", url)
    return DEFAULT_ERROR_MESSAGE, DEFAULT_ERROR_MESSAGE


async def get_keyword_news(keyword: str) -> list[str]:
    href_links: list[str] = []
    limit_cnt = 10
    origin_url = f"https://search.naver.com/search.naver?where=news&query={keyword}"

    try:
        async with _create_client() as client:
            response = await client.get(origin_url)
            response.raise_for_status()
    except httpx.HTTPError as exc:
        print(f"[Crawler] 뉴스 검색 결과 요청 실패: {exc}")
        return href_links

    soup = BeautifulSoup(response.text, "html.parser")
    naver_spans = soup.find_all("span", string="네이버뉴스")

    for news in naver_spans:
        anchor_tag = news.find("a")
        if anchor_tag:
            href = anchor_tag.get("href")
            href_links.append(href)

        if len(href_links) >= limit_cnt:
            break

    return href_links


async def get_news_from_naver(keyword: str, urls: list[str]) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    if not urls:
        return results

    async with _create_client() as client:
        for url in urls:
            try:
                response = await client.get(url)
                response.raise_for_status()
            except httpx.HTTPError as exc:
                print(f"[Crawler] 기사 요청 실패 ({url}): {exc}")
                results.append(
                    {
                        "keyword": keyword,
                        "link": url,
                        "title": DEFAULT_ERROR_MESSAGE,
                        "content": DEFAULT_ERROR_MESSAGE,
                    }
                )
                continue

            soup = BeautifulSoup(response.text, "html.parser")
            title, content = _parse_article(url, soup)
            results.append(
                {
                    "keyword": keyword,
                    "link": url,
                    "title": title,
                    "content": content,
                }
            )
            await asyncio.sleep(0.2)
    return results


async def news_crawling(keyword: str) -> list[dict[str, str]]:
    href_links = await get_keyword_news(keyword)
    news_results = await get_news_from_naver(keyword, href_links)
    return news_results


print("=== Crawler Ready ===")
