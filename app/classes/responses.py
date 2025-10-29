"""
응답과 관련된 클래스들 입니다.
"""

from dataclasses import dataclass


@dataclass
class SearchResult:
    """
    키워드에 대한 검색 결과를 담당하는 클래스입니다.
    Attributes:
      keyword (str):
      title (str):
      link (str):
      content (str):
    """

    keyword: str
    title: str
    link: str
    content: str


@dataclass
class SearchResultOutput:
    """
    검색에 대한 응답 클래스입니다.
    """

    keyword: str
    description: str
    content: str
    tags: list[str]
    category: str
    refered: list[str]
