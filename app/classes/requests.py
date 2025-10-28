"""
요청과 관련된 클래스들 입니다.
"""

from dataclasses import dataclass


@dataclass
class SearchRequest:
    """
    키워드 검색할 때 Spring boot 서버가 보내줄 데이터 입니다.
    Attributes:
      keyword (str):
    """

    keyword: str
