from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()


# embedding = OpenAIEmbeddings(
#     model="text-embedding-3-small"
# )

# db = FAISS.load_local(
#     "vectordb",
#     embedding,
#     allow_dangerous_deserialization=True
# )

# results = db.similarity_search(
#     "What was Apple's revenue?"
# )

# print(results[0].page_content)

from src.rag_engine import ask_question

answer, docs = ask_question(
    "What was Apple's revenue?"
)

print(answer)