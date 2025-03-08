"""LLM module.

# Proxy LLM
LiteLLM can be used for LLM inference.
- Model providers: https://docs.litellm.ai/docs/providers
"""

from langchain_core.messages import AIMessage
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from config import CFG_ENGINE
from src.common.logger import log_info
from src.common.timer import T


# Initialize ChatOpenAI client once at module level
if CFG_ENGINE.inference.llm.use_proxy:
    llm = ChatOpenAI(
        model=CFG_ENGINE.inference.llm.model,
        base_url=CFG_ENGINE.inference.llm.proxy.base_url,
    )
    embeddings = OpenAIEmbeddings()
else:
    llm = ChatOpenAI(model=CFG_ENGINE.inference.llm.model)
    embeddings = OpenAIEmbeddings()


@T
def completion(messages: list[dict | tuple]) -> AIMessage:
    """Get completion from LLM."""
    response = llm.invoke(messages)

    # Log metadata
    log_info("Token usage:"), log_info(response.usage_metadata)
    return response


async def acompletion(messages: list[dict | tuple]) -> AIMessage:
    """Get completion from LLM asynchronously."""
    response = await llm.ainvoke(messages)

    # Log metadata
    log_info("Token usage:"), log_info(response.usage_metadata)
    return response


if __name__ == "__main__":
    messages = [("user", "안녕! 네 이름이 뭐니?")]
    response = completion(messages)
    print(response.content)
