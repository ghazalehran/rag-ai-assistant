import os
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
from config import CHUNK_SIZE, CHUNK_OVERLAP

load_dotenv()

def load_vectorstore(pdf_name):
    # Build paths
    pdf_path = f"documents/{pdf_name}"
    db_dir = f"chroma_dbs/{os.path.splitext(pdf_name)[0]}"

    embeddings = OpenAIEmbeddings()

    if os.path.exists(db_dir) and os.listdir(db_dir):
        print(f"📦 Loading existing vectorstore for {pdf_name}")
        vectorstore = Chroma(persist_directory=db_dir, embedding_function=embeddings)
        split_docs = None  # Already embedded
    else:
        print(f"📄 Creating vectorstore for {pdf_name}")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
        split_docs = splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(
            documents=split_docs,
            embedding=embeddings,
            persist_directory=db_dir
        )
        vectorstore.persist()

    return vectorstore, split_docs
