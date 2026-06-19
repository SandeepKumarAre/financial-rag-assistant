import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DATA_PATH = "data"
VECTOR_DB_PATH = "vectordb"

documents = []

for file in os.listdir(DATA_PATH):

    if file.endswith(".pdf"):

        filename = file.lower()

        if "apple" in filename:
            company = "Apple"

        elif "microsoft" in filename:
            company = "Microsoft"

        else:
            company = "Unknown"


        pdf_path = os.path.join(DATA_PATH, file)

        print(f"Loading {file}")

        loader = PyPDFLoader(pdf_path)

        docs = loader.load()

        for doc in docs:

            doc.metadata["source_file"] = file
            doc.metadata["page_number"] = (
                doc.metadata.get("page", 0) + 1
            )
            doc.metadata["company"] = company

        documents.extend(docs)

print(f"Total Pages Loaded: {len(documents)}")


splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(documents)

print(f"Total Chunks: {len(chunks)}")

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

vectorstore = FAISS.from_documents(
    chunks,
    embeddings
)

vectorstore.save_local(VECTOR_DB_PATH)

print("Vector DB Created Successfully")