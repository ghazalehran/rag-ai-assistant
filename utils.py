from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from config import TEMPERATURE, K_RETRIEVAL, IMPORTANT_QUESTION_KEYWORDS

llm = OpenAI(temperature=TEMPERATURE)

strict_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant analyzing a scientific research paper.

Use ONLY the context below. Do not rely on outside knowledge or assumptions.

Rules:
- If the answer is stated, quote or summarize.
- If an equivalent term is used (e.g., "objective" instead of "hypothesis"), mention that.
- If no answer, say exactly: "Not found in the provided context."

Context:
{context}

Question: {question}
Answer:
"""
)

fallback_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant summarizing a scientific research paper.

Use the context below to answer clearly. If not explicitly stated, infer or summarize what the study suggests.

Context:
{context}

Question: {question}
Answer:
"""
)

qa_chain_strict = load_qa_chain(llm=llm, chain_type="stuff", prompt=strict_prompt)
qa_chain_flexible = load_qa_chain(llm=llm, chain_type="stuff")
qa_chain_fallback = LLMChain(llm=llm, prompt=fallback_prompt)

def get_best_answer(query, vectorstore, split_docs):
    docs = vectorstore.similarity_search(query, k=K_RETRIEVAL)
    strict_answer = qa_chain_strict.run(input_documents=docs, question=query)

    needs_fallback = (
        "Not found" in strict_answer
        or len(strict_answer.strip()) < 10
        or any(key in query.lower() for key in IMPORTANT_QUESTION_KEYWORDS)
    )

    if needs_fallback:
        print("⚠️ Using fallback context...")
        fallback_chunks = [
            doc for doc in split_docs or []
            if any(word in doc.page_content.lower() for word in ["introduction", "conclusion"])
        ]
        fallback_context = "\n\n".join(doc.page_content for doc in fallback_chunks)
        return qa_chain_fallback.run({"context": fallback_context, "question": query})

    return strict_answer
