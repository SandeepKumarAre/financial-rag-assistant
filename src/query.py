import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_classic.chains.retrieval_qa.base import RetrievalQA
# from langchain.chains import RetrievalQA

from langchain_classic.prompts import PromptTemplate

# import streamlit as st

# st.title("Financial RAG Assistant")

# question = st.text_input(
#     "Ask a question"
# )

# if question:
#     st.write(question)

load_dotenv()

VECTOR_DB_PATH = "vectordb"

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)


template = """
You are a financial analyst.

Answer ONLY using the supplied context.

If the answer is not found,
respond:

'I could not find that information
in the provided documents.'

Context:
{context}

Question:
{question}

Answer: 
"""

db = FAISS.load_local(
    VECTOR_DB_PATH,
    embeddings,
    allow_dangerous_deserialization=True
)

# retriever = db.as_retriever(
#     search_kwargs={"k": 5}
# )
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)


llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

prompt = PromptTemplate(
    template=template,
    input_variables=["context", "question"]
)

# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     retriever=retriever,
#     return_source_documents=True
# )

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={
        "prompt": prompt
    }
)

query = input("Ask a question: ")

result = qa_chain.invoke(
    {"query": query}
)


# question = st.text_input(
#     "Ask a question"
# )

# if question:

#     result = qa_chain.invoke(
#         {"query": question}
#     )

#     st.subheader("Answer")

#     st.write(result["result"])

print("\nANSWER")
print("=" * 50)
print(result["result"])

print("\nSOURCES")
print("=" * 50)

for doc in result["source_documents"]:
    # print(
    #     f"File: {doc.metadata.get('source_file')}"
    # )
    print(
    f"""
    File : {doc.metadata.get('source_file')}
    Page : {doc.metadata.get('page_number')}
    """
    )