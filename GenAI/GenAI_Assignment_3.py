import os
import wikipedia
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    groq_api_key=GROQ_API_KEY,
    temperature=0
)

template = ChatPromptTemplate([
    ("system", "You are a history expert assistant. Answer only using the retrieved Wikipedia passages."),
    ("placeholder", "{conversation}"),
    ("human", "{question}")
])

st.title("Wikipedia Search-Enhanced Historical Q&A")

if "messages" not in st.session_state:
    st.session_state.messages = []


for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)


user_input = st.chat_input("Enter your historical question:")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    

    try:
        search_results = wikipedia.search(user_input, results=3)
        passages = []
        for title in search_results:
            try:
                page = wikipedia.page(title)
                passages.append(page.content[:1000])  # take first 1000 chars
            except Exception:
                continue
        retrieved_passages = "\n\n".join(passages) if passages else "No passages found."
    except Exception as e:
        retrieved_passages = f"Error fetching Wikipedia content: {e}"

    prompt = template.invoke({
        "conversation": st.session_state.messages,
        "question": f"{user_input}\n\nWikipedia passages:\n{retrieved_passages}"
    })

    with st.chat_message("assistant"):
        result = llm.stream(prompt)
        ai_response = st.write_stream(result)
    
    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.messages.append(AIMessage(content=ai_response))