from loader import load_vectorstore
from utils import get_best_answer

questions = [
    "What is the main goal of the research?",
    "What is the main hypothesis or research question?",
    "Summarize the findings of this study.",
    "What are the main conclusions drawn in the paper?",
    "What data or participants were used in the study?",
    "What methods or models were applied?",
    "What is Self-Supervised Learning in the context of this research?",
    "Did the SSL model outperform the baseline?",
    "How is this research relevant to autism?",
    "What limitations does the paper acknowledge?"
]

# Change this to test other PDFs
pdf_filename = "TWDpdf.pdf"

vectorstore, split_docs = load_vectorstore(pdf_filename)

for i, question in enumerate(questions, 1):
    print(f"\n{'='*80}")
    print(f"🔹 Question {i}: {question}")
    answer = get_best_answer(question, vectorstore, split_docs)
    print(f"\n🧠 Answer:\n{answer}")