from langchain_openai import ChatOpenAI

from app.config import Settings, get_settings


def create_llm(settings: Settings | None = None) -> ChatOpenAI:
    """Create a chat model through any OpenAI-compatible endpoint.

    OpenAI is the default when LLM_URL is empty. Providers such as Gemini's
    OpenAI-compatible API, OpenRouter, Groq, Together, and local gateways can
    be selected by setting LLM_URL, LLM_API_KEY, and LLM_MODEL.
    """
    resolved = settings or get_settings()
    if not resolved.llm_api_key:
        raise RuntimeError(
            "LLM_API_KEY is required to create the configured LLM")

    options: dict[str, str] = {
        "api_key": resolved.llm_api_key,
        "model": resolved.llm_model,
    }
    if resolved.llm_url:
        options["base_url"] = resolved.llm_url.rstrip("/")

    return ChatOpenAI(**options)
