import os
import pickle
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from config import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    EMBEDDING_PROVIDER,
    VECTORSTORE_BACKEND,
    USE_HF_SECRETS,
)

# Load env if not using hosted secrets
if not USE_HF_SECRETS:
    from dotenv import load_dotenv
    load_dotenv()

# Load embedding model
if EMBEDDING_PROVIDER == "openai":
    from langchain.embeddings import OpenAIEmbeddings
    embeddings = OpenAIEmbeddings()
elif EMBEDDING_PROVIDER == "huggingface":
    from langchain.embeddings import HuggingFaceEmbeddings
    embeddings = HuggingFaceEmbeddings()
else:
    raise ValueError(f"Unsupported EMBEDDING_PROVIDER: {EMBEDDING_PROVIDER}")

# Load vectorstore (FAISS or Chroma)
def load_vectorstore(pdf_name):
    pdf_path = f"documents/{pdf_name}"
    base_name = os.path.splitext(pdf_name)[0]

    if VECTORSTORE_BACKEND == "chroma":
        from langchain.vectorstores import Chroma
        db_dir = f"chroma_dbs/{base_name}"
        if os.path.exists(db_dir) and os.listdir(db_dir):
            print(f"📦 Loading Chroma vectorstore for {pdf_name}")
            vectorstore = Chroma(persist_directory=db_dir, embedding_function=embeddings)
            return vectorstore, None

    elif VECTORSTORE_BACKEND == "faiss":
        from langchain.vectorstores import FAISS
        db_path = f"faiss_dbs/{base_name}"
        index_path = f"{db_path}.pkl"

        if os.path.exists(f"{db_path}.faiss") and os.path.exists(index_path):
            print(f"📦 Loading FAISS vectorstore for {pdf_name}")
            with open(index_path, "rb") as f:
                docs = pickle.load(f)
            vectorstore = FAISS.load_local(db_path, embeddings, allow_dangerous_deserialization=True)
            return vectorstore, None

    else:
        raise ValueError(f"Unsupported VECTORSTORE_BACKEND: {VECTORSTORE_BACKEND}")

    # Create vectorstore if none exists
    print(f"📄 Creating vectorstore for {pdf_name}")
    loader = PyPDFLoader(pdf_path)
    raw_docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    split_docs = splitter.split_documents(raw_docs)

    if VECTORSTORE_BACKEND == "chroma":
        os.makedirs(f"chroma_dbs/{base_name}", exist_ok=True)
        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,
            persist_directory=f"chroma_dbs/{base_name}"
        )
        vectorstore.persist()

    elif VECTORSTORE_BACKEND == "faiss":
        os.makedirs("faiss_dbs", exist_ok=True)
        vectorstore = FAISS.from_documents(split_docs, embedding=embeddings)
        vectorstore.save_local(f"faiss_dbs/{base_name}")

        # Save original docs to allow context fallback later
        with open(f"faiss_dbs/{base_name}.pkl", "wb") as f:
            pickle.dump(split_docs, f)

    return vectorstore, split_docs
