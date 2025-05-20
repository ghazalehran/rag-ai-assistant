# app.py (for Streamlit)
import streamlit as st
import os
import shutil
from loader import load_vectorstore
from utils import get_best_answer

st.set_page_config(page_title="Gazara", layout="wide")

st.title("🧠 Gazara: Research Assistant")

pdf_file = st.file_uploader("📄 Upload your PDF", type=["pdf"])

question = st.text_input("❓ Ask a question about the paper:")

dev_mode = st.checkbox("🧪 Dev Mode")

if st.button("Get Answer") and pdf_file and question:
    filename = pdf_file.name
    save_path = os.path.join("documents", filename)
    with open(save_path, "wb") as f:
        f.write(pdf_file.read())

    try:
        if dev_mode:
            st.markdown(f"🧪 [Dev Mode] Would answer: '{question}'")
        else:
            vectorstore, split_docs = load_vectorstore(filename)
            answer = get_best_answer(question, vectorstore, split_docs)
            st.markdown(f"**🧠 Answer:** {answer}")
    except Exception as e:
        st.error(f"⚠️ Error: {e}")
