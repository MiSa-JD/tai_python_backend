from langchain.schema import Document
from app.ai.config.config import THRESHOLD, vstore, splitter
from app.classes.metadata import Metadata
from app.classes.responses import SearchResult


# VDB에 저장된 문서 묶음 검색해오기
def search_documents(keyword: str) -> list[Document]:
    scored = vstore.similarity_search_with_score(keyword, k=20)

    filtered = [doc for doc, score in scored if score <= THRESHOLD]
    return filtered


# 검색 후 프롬프트도 만들기
def get_prompt_on_retrieve(keyword: str, prompt: str) -> str:
    search_results = search_documents(keyword=keyword)

    # 프롬프트에 내용 삽입하기
    result = prompt
    for items in search_results:
        result += "\n" + items.page_content

    return result


# contents를 스플리터로 자르고 메타데이터 붙이기
def split_documents(contents: list[str], metadatas: list[Metadata]):
    docs: list[Document] = []

    for i in range(len(contents)):
        splits = splitter.create_documents(
            texts=[contents[i]],
            metadatas=[
                {
                    "keyword": metadatas[i].keyword,
                    "link": metadatas[i].link,
                }
            ],
        )
        docs.extend(splits)
    return docs


# SearchResult로 가져온 문서들을 contents와 metadatas로 분리
def embed_documents(datas: list[SearchResult]):
    # 데이터를 content와 메타데이터로 분리
    # print(datas)
    contents: list[str] = [
        ("# " + data["title"] + "\n" + data["content"]) for data in datas
    ]
    metadatas: list[Metadata] = [
        Metadata(data["keyword"], data["link"]) for data in datas
    ]

    docs = split_documents(contents=contents, metadatas=metadatas)

    # 벡터 스토어에 데이터 저장
    vstore.add_documents(docs)

    return {"result": "complete"}
