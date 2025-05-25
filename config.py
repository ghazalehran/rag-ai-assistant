import os

# === Deployment Environment ===
USE_HF_SECRETS = os.getenv("USE_HF_SECRETS", "True").lower() == "true"  # can be set via env var

if not USE_HF_SECRETS:
    from dotenv import load_dotenv
    load_dotenv()

# === API Keys ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

# === Embedding / Vectorstore / Model Settings ===
VECTORSTORE_BACKEND = os.getenv("VECTORSTORE_BACKEND", "chroma")  # "faiss" or "chroma"
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "openai")   # "openai" or "huggingface"
LLM_BACKEND = os.getenv("LLM_BACKEND", "openai")                  # "openai", "huggingface", etc.

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", 800))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", 100))
K_RETRIEVAL = int(os.getenv("K_RETRIEVAL", 5))
TEMPERATURE = float(os.getenv("TEMPERATURE", 0.2))

FALLBACK_SECTIONS = ["introduction", "conclusion"]
IMPORTANT_QUESTION_KEYWORDS = [
    "findings", "summary", "conclusion", "autism", "hypothesis", "objective"
]

# === Model Names ===
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
HF_MODEL = os.getenv("HF_MODEL", "mistralai/Mistral-7B-Instruct-v0.2")
