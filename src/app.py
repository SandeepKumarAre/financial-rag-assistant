# # import streamlit as st

# # st.title("Financial RAG Assistant")

# # question = st.text_input(
# #     "Ask a question"
# # )

# # if question:
# #     st.write(question)


# # from dotenv import load_dotenv

# # from langchain_openai import OpenAIEmbeddings
# # from langchain_community.vectorstores import FAISS

# # load_dotenv()

# # embeddings = OpenAIEmbeddings(
# #     model="text-embedding-3-small"
# # )

# # db = FAISS.load_local(
# #     "vectordb",
# #     embeddings,
# #     allow_dangerous_deserialization=True
# # )

# # retriever = db.as_retriever(
# #     search_kwargs={"k": 5}
# # )

# # from langchain_openai import ChatOpenAI

# # llm = ChatOpenAI(
# #     model="gpt-4o",
# #     temperature=0
# # )

# # # from langchain.chains import RetrievalQA

# # from langchain_classic.chains.retrieval_qa.base import RetrievalQA

# # qa_chain = RetrievalQA.from_chain_type(
# #     llm=llm,
# #     retriever=retriever,
# #     return_source_documents=True
# # )

# # question = st.text_input(
# #     "Ask a question"
# # )

# # if question:

# #     result = qa_chain.invoke(
# #         {"query": question}
# #     )

# #     st.subheader("Answer")

# #     st.write(result["result"])

# # st.subheader("Sources")

# # for doc in result["source_documents"]:

# #     st.write(
# #         f"""
# #         File:
# #         {doc.metadata.get('source_file')}

# #         Page:
# #         {doc.metadata.get('page_number')}
# #         """
# #     )

# import streamlit as st

# if "messages" not in st.session_state:

#     st.session_state.messages = []

# from rag_engine import ask_question

# st.title("Financial RAG Assistant")

# for message in st.session_state.messages:

#     with st.chat_message(
#         message["role"]
#     ):

#         st.markdown(
#             message["content"]
#         )


# # prompt = st.chat_input(
# #     "Ask a question"
# # )

# prompt = st.chat_input(
#     "Ask a question"
# )

# if prompt:

#     st.session_state.messages.append(
#         {
#             "role": "assistant",
#             "content": prompt
#         }
#     )

#     with st.chat_message("assistant"):

#         st.markdown(prompt)

#     answer, docs = ask_question(prompt)

#     st.write(answer)

#     st.markdown("### Sources")

#     for doc in docs:

#         source = doc.metadata.get(
#             "source_file"
#         )

#         page = doc.metadata.get(
#             "page_label"
#         )

#         st.markdown(
#             f"- {source} (Page {page})"
#         )


#     # st.subheader("Sources")

#     # for doc in docs:

#     #     source = doc.metadata.get("source_file")

#     #     page = doc.metadata.get("page_label")

#     #     st.write(
#     #         f"{source} (Page {page})"
#     #     )

    

import streamlit as st

from rag_engine import ask_question

if "messages" not in st.session_state:
    st.session_state.messages = []

st.title("Financial RAG Assistant")

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input(
    "Ask a question"
)

if prompt:

    # User message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG call

    answer, docs = ask_question(question=prompt,chat_history=st.session_state.messages)

    # Save assistant response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):

        st.markdown(answer)

        st.markdown("### Sources")

        for doc in docs:

            source = doc.metadata.get(
                "source_file"
            )

            page = doc.metadata.get(
                "page_label"
            )

            st.markdown(
                f"- {source} (Page {page})"
            )

