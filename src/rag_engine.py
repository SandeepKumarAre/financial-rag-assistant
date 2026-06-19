from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from guardrails import validate_question

load_dotenv()

embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

db = FAISS.load_local(
    "vectordb",
    embeddings,
    allow_dangerous_deserialization=True
)
retriever = db.as_retriever(
    search_kwargs={"k":5}
)

llm = ChatOpenAI(
    model="gpt-4o",
    temperature=0
)

def detect_company(question):

    question = question.lower()

    if "apple" in question:
        return "Apple"

    if "microsoft" in question:
        return "Microsoft"

    return None

def ask_question(question, chat_history=None):
    history_text = ""

    if chat_history:

        for msg in chat_history[-6:]:

            history_text += (
                f"{msg['role']}: {msg['content']}\n"
            )

    if not validate_question(question):

        return (
            "Question violates security policy.",
            []
        )
    ### RE-Write the Prompts.

    rewrite_prompt = f"""
            You are a query rewriting assistant.

            Using the conversation history,
            rewrite the user's latest question
            into a complete standalone question.

            Conversation:

            {history_text}

            Latest Question:

            {question}

            Standalone Question:
            """
    
    rewritten_question = llm.invoke(rewrite_prompt).content

    # print("\nRewritten Question:",rewritten_question)


    print("\n" + "=" * 60)

    print("Original Question:")
    print(question)

    print("\nRewritten Question:")
    print(rewritten_question)

    print("=" * 60)


    # docs = retriever.invoke(rewritten_question)

    company = detect_company(
        rewritten_question
    )

    if company:
        docs = db.similarity_search(
            rewritten_question,
            k=5,
            filter={"company": company}
        )
    else:
        print("without filter")
        docs = retriever.invoke(
            rewritten_question
    )
        
    print(docs)
    # results = []
    # for doc, score in docs:
    #     print(
    #         f"""
    #         File:
    #         {doc.metadata.get('source_file')}

    #         Score:
    #         {score}
    #         """
    #             )
    #     results.append(doc)
    
    # print(results)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
            You are a financial analyst.

            Answer ONLY using the supplied context.

            If answer is unavailable, say:

            'I could not find that information in the provided documents.'

            Context:
            {context}

            Question:
            {rewritten_question}

            Answer:
            """

    response = llm.invoke(prompt)

    return response.content, docs



# def ask_question(question):

#     docs = retriever.invoke(question)

#     context = "\n\n".join(
#         [doc.page_content for doc in docs]
#     )

#     prompt = f"""
#             You are a financial analyst.

#             Use only the supplied context.

#             Context:
#             {context}

#             Question:
#             {question}

#             Answer:
#             """

#     response = llm.invoke(prompt)
#     return response.content, docs