from config import (
    LLM_BACKEND,
    OPENAI_MODEL,
    HF_MODEL,
    HUGGINGFACEHUB_API_TOKEN,
    TEMPERATURE
)

from langchain.chat_models import ChatOpenAI
from langchain.llms import HuggingFaceHub


def get_llm(temperature=TEMPERATURE):
    if LLM_BACKEND == "openai":
        return ChatOpenAI(
            model=OPENAI_MODEL,
            temperature=temperature
        )
    elif LLM_BACKEND == "huggingface":
        return HuggingFaceHub(
            repo_id=HF_MODEL,
            model_kwargs={"temperature": temperature, "max_new_tokens": 512},
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
        )
    else:
        raise ValueError(f"Unsupported LLM_BACKEND: {LLM_BACKEND}")
