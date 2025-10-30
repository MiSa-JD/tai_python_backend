from app.ai.config.models import llm_analize, llm_classify, llm_summarize, llm_validate
from app.ai.prompts import (
    analyst_prompt,
    validator_prompt,
    classifier_prompt,
    summarizer_prompt,
    analyst_input_prompt,
    analyst_form,
    validator_form,
)
from langchain.schema import Document, SystemMessage, HumanMessage


def analyst_llm(keyword: str, docs: list[Document], summaries: list[str]) -> str:
    """
    분석 llm 호출 함수
    """
    messages = [
        SystemMessage(content=analyst_prompt(keyword, analyst_form)),
        HumanMessage(content=analyst_input_prompt(docs, summaries)),
    ]

    # invoke()는 ChatModel 표준 인터페이스입니다.
    result = llm_analize.invoke(messages)

    # result는 보통 AIMessage 객체이며 .content에 텍스트가 들어 있습니다.
    return result.content.strip()


def validator_llm(prompt: str, keyword: str) -> str:
    """
    검증 llm 호출 함수
    """
    messages = [
        SystemMessage(content=validator_prompt(keyword, validator_form)),
        HumanMessage(content=prompt),
    ]

    # invoke()는 ChatModel 표준 인터페이스입니다.
    result = llm_validate.invoke(messages)

    return result.content.strip()


def summarizer_llm(prompt: str) -> str:
    """
    요약 llm 호출 함수
    """
    messages = [
        SystemMessage(content=summarizer_prompt),
        HumanMessage(content=prompt),
    ]

    result = llm_summarize.invoke(messages)

    # result는 보통 AIMessage 객체이며 .content에 텍스트가 들어 있습니다.
    return result.content.strip()


def classifier_llm(prompt: str) -> str:
    """
    분류 llm 호출 함수
    """
    messages = [
        SystemMessage(content=classifier_prompt),
        HumanMessage(content=prompt),
    ]

    result = llm_classify.invoke(messages)

    # result는 보통 AIMessage 객체이며 .content에 텍스트가 들어 있습니다.
    return result.content.strip()
