
# 🧠 AI Research Assistant — RAG-based QA for Scientific PDFs

This is a modular **Retrieval-Augmented Generation (RAG)** app built with **LangChain**, **FAISS/Chroma**, and **OpenAI/Hugging Face** models. It enables you to upload research PDFs and ask intelligent, context-aware questions — powered by embeddings, vector search, and LLMs.

> ⚙️ Designed to be scalable, extensible, and cloud-deployable (Hugging Face, Streamlit). Ideal for demonstrating production-grade NLP capabilities.

---

## 📸 Live Demo Interface

<img src="static\gradio-interface.png" alt="Gradio UI Screenshot" width="100%">

---

## 🚀 Key Features

- ✅ Upload any PDF research paper
- ✂️ Smart chunking & vector embedding
- 🔎 Search via **FAISS** (default) or **ChromaDB**
- 🧠 Flexible LLM backends: `OpenAI`, `Hugging Face`, or your own
- 🔍 Dual QA strategy: strict context-only + fallback summarization
- 💾 Cached vectorstores — no reprocessing
- 🧪 Dev mode for testing without LLM cost
- 🌐 Gradio interface included for rapid UI

---

## 🛠️ Skills & Stack Highlights

- **Python**, **LangChain**, **LLMs**, **RAG**
- OpenAI API, Hugging Face Hub models
- FAISS, ChromaDB, PyPDFLoader
- Gradio UI, .env + Hugging Face secrets
- Local + cloud deployability

---

## 📁 Folder Structure

```
rag-ai-assistant/
├── app_local.py           # Gradio UI for local testing
├── main.py                # Optional CLI/deployment entry point
├── loader.py              # Vectorstore creator/loader
├── utils.py               # QA chain logic with fallback
├── llm_provider.py        # LLM loader (OpenAI / HF)
├── config.py              # Centralized config for env + models
├── documents/             # Drop your PDFs here
├── faiss_dbs/             # Vectorstore (FAISS)
├── chroma_dbs/            # Vectorstore (Chroma)
├── requirements.txt
└── .env                   # Only used locally
```

---

## ⚙️ Quick Setup

### 1. Clone & Set Up

```bash
git clone https://github.com/ghazalehran/rag-ai-assistant.git
cd rag-ai-assistant
python -m venv rag-env
source rag-env/bin/activate  # Windows: rag-env\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file (used locally only):

```env
OPENAI_API_KEY=sk-...
HUGGINGFACEHUB_API_TOKEN=hf-...
```

> For Hugging Face or Streamlit cloud deploy, use **secret management UI**.

---

## 🖥️ Run the Gradio App

```bash
python app_local.py
```

This opens a local Gradio interface in your browser where you can:

- Upload a PDF
- Ask a natural language question
- Get an intelligent answer from the LLM

---

## 🔄 Configurable Options

All configurations are managed via `config.py`:

| Option               | Description                                |
|----------------------|--------------------------------------------|
| `LLM_BACKEND`        | `"openai"` / `"huggingface"`               |
| `VECTORSTORE_BACKEND`| `"faiss"` / `"chroma"`                     |
| `CHUNK_SIZE`         | Default: `800` tokens                      |
| `TEMPERATURE`        | LLM creativity (default: `0.2`)            |
| `USE_HF_SECRETS`     | `True` if deploying on Hugging Face Cloud  |

---

## ✅ Example Models Used

- **OpenAI**: `gpt-4`, `gpt-3.5-turbo`
- **Hugging Face**: [`mistralai/Mistral-7B-Instruct-v0.2`](https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.2)

---

## 📄 License

MIT — free for personal, academic, or professional use.

---

## 🙋‍♂️ Questions?

Feel free to open an issue or connect on [LinkedIn](https://linkedin.com).

---