"""Inference module."""

from langchain.globals import set_llm_cache
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_elasticsearch import ElasticsearchCache
from langchain_core.cache import InMemoryCache

from config import CFG_SERVICE, SERVICE_NAME
from src.common.utils import SingletonBase
from src.common.logger import log_success, log_warning


# Cache LLM responses
_llm_cache_init = False


def init_llm_cache() -> None:
    """Initialize LLM cache."""
    global _llm_cache_init
    if _llm_cache_init:
        return

    try:
        param = {
            "es_url": CFG_SERVICE.elasticsearch.url,
            "es_user": CFG_SERVICE.elasticsearch.user,
            "es_password": CFG_SERVICE.elasticsearch.password,
            "index_name": CFG_SERVICE.elasticsearch.llm_cache.index.name,
            "metadata": {"service": SERVICE_NAME},
        }
        cache = ElasticsearchCache(**param)
        set_llm_cache(cache)
        _llm_cache_init = True
        log_success("LLM cache using Elasticsearch has been successfully enabled.")
    except Exception as e:
        cache = InMemoryCache()
        set_llm_cache(cache)
        _llm_cache_init = True
        log_warning(f"Failed to connect to Elasticsearch: {e}")
        log_success("LLM cache using InMemoryCache has been successfully enabled.")


class LLMManager(SingletonBase):
    """LLM manager.

    Attributes:
        model: LLM model
        invoke_config: Invoke config for LLM
    """

    @classmethod
    def _generate_instance_key(cls, provider: str) -> tuple:
        return (provider,)

    def _init_once(self, provider: str) -> None:
        """Initialize LLM manager."""
        init_llm_cache()

        self.provider = provider
        self.cfg = CFG_SERVICE.inference.llm.providers[provider]
        self.model = self._get_model()
        self.invoke_config = self._get_invoke_config()

    def _get_model(self) -> ChatOpenAI:
        """Get LLM model."""
        return ChatOpenAI(**self.cfg["model_config"])

    def _get_invoke_config(self) -> dict:
        """Get invoke config for LLM."""
        return {
            "max_concurrency": self.cfg.max_concurrency,
        }


class EmbeddingsManager(SingletonBase):
    """Embeddings manager.

    Attributes:
        model: Embeddings model
    """

    @classmethod
    def _generate_instance_key(cls, provider: str) -> tuple:
        return (provider,)

    def _init_once(self, provider: str) -> None:
        self.provider = provider
        self.cfg = CFG_SERVICE.inference.embeddings.providers[provider]
        self.model = self._get_model()

    def _get_model(self) -> OpenAIEmbeddings:
        """Get embeddings model."""
        return OpenAIEmbeddings(**self.cfg["model_config"])
