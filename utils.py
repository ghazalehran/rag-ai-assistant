from typing import List, Optional
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.schema.document import Document

from config import (
    TEMPERATURE,
    K_RETRIEVAL,
    IMPORTANT_QUESTION_KEYWORDS,
    FALLBACK_SECTIONS,
)

from llm_provider import get_llm

# Constants
FALLBACK_CHUNK_LIMIT = 5

# Load LLM based on config
llm = get_llm(temperature=TEMPERATURE)

# Strict QA prompt
strict_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant analyzing a scientific research paper.

Use ONLY the context below. Do not rely on outside knowledge or assumptions.

Rules:
- Quote or summarize directly from the context if possible.
- Mention if synonyms are used (e.g., "objective" instead of "hypothesis").
- If the answer is not present, say: "Not found in the provided context."

Context:
{context}

Question: {question}
Answer:
"""
)

# Fallback prompt for inferred answers
fallback_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant summarizing a scientific research paper.

Use the context below to answer clearly and informatively. If not explicitly stated, infer or summarize what the paper suggests.

Context:
{context}

Question: {question}
Answer:
"""
)

# QA chains
qa_chain_strict = load_qa_chain(llm=llm, chain_type="stuff", prompt=strict_prompt)
qa_chain_flexible = load_qa_chain(llm=llm, chain_type="stuff")  # Unused but reserved
qa_chain_fallback = LLMChain(llm=llm, prompt=fallback_prompt)


def get_best_answer(
    query: str,
    vectorstore,
    split_docs: Optional[List[Document]]
) -> str:
    docs = vectorstore.similarity_search(query, k=K_RETRIEVAL)

    if not docs:
        return "⚠️ No relevant content found in vectorstore."

    strict_answer = qa_chain_strict.run(input_documents=docs, question=query)

    needs_fallback = (
        "Not found" in strict_answer
        or len(strict_answer.strip()) < 10
        or any(keyword in query.lower() for keyword in IMPORTANT_QUESTION_KEYWORDS)
    )

    if needs_fallback and split_docs:
        print("⚠️ Using fallback context...")

        fallback_chunks = [
            doc for doc in split_docs
            if any(section in doc.page_content.lower() for section in FALLBACK_SECTIONS)
        ]

        fallback_context = "\n\n".join(
            doc.page_content for doc in fallback_chunks[:FALLBACK_CHUNK_LIMIT]
        )

        return qa_chain_fallback.run({
            "context": fallback_context,
            "question": query
        })

    return strict_answer
