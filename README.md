# 🧠 AI Research Assistant — RAG with LangChain

A Retrieval-Augmented Generation (RAG) assistant for reading, understanding, and answering questions about scientific papers in PDF format. Built with [LangChain](https://www.langchain.com/), ChromaDB, and OpenAI’s API. Designed to be modular, scalable, and deployable.

---

## ✨ Features

- 📄 Upload and parse **multiple PDFs**
- ✂️ Automatically **chunk and embed** documents
- 🔍 Perform **semantic search** with ChromaDB
- 🤖 Ask **natural language questions**
- 💡 Includes **strict QA + fallback summarization logic** for reliable answers
- 📁 Vectorstore caching for re-use without re-embedding
- 🚀 Flexible architecture: CLI or Gradio-ready

---

## 📂 Project Structure

```
rag-ai-assistant/
├── main.py                # Main QA runner
├── utils.py               # Chains and fallback logic
├── vectorstore_loader.py  # Loads or creates vectorstores per PDF
├── config.py              # Settings for chunking, retrieval, etc.
├── documents/             # Drop your PDFs here
├── chroma_dbs/            # Vectorstores per PDF (ignored by Git)
├── .env                   # OpenAI API key
└── requirements.txt
```

---

## ⚙️ Setup Instructions

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/rag-ai-assistant.git
   cd rag-ai-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv rag-env
   source rag-env/bin/activate  # or rag-env\Scripts\activate on Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set your OpenAI API key**

   Create a `.env` file:
   ```
   OPENAI_API_KEY=sk-...
   ```

5. **Add your PDF(s)**

   Drop one or more `.pdf` files into the `documents/` folder.

---

## 🧪 Run the Assistant

```bash
python main.py
```

Then follow the CLI prompts or view the output answers in terminal.

---

## 🧠 Coming Soon

- 🌐 Web UI with Gradio
- 🧾 Graded answer confidence and citation tracing
- 🗂 Support for document sets / paper collections
- 🧠 Local LLM (e.g. Mixtral or llama.cpp)

---

## 📄 License

MIT License — free to use, improve, and adapt.

---

## 🙋‍♀️ Questions or Feedback?

Feel free to open an issue or reach out on [LinkedIn](https://www.linkedin.com/)!