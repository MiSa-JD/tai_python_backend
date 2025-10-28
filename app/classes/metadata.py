"""
메타 데이터 클래스
"""

from dataclasses import dataclass


@dataclass
class Metadata:
    """
    Attributes:
      keyword (str):
      link (str):
    """

    keyword: str
    link: str
