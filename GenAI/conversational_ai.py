
from langchain_groq import ChatGroq 
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

llm = ChatGroq(
    # model="qwen/qwen3-32b", # llama-3.1-8b-instant
    model="llama-3.1-8b-instant", # llama-3.1-8b-instant
    temperature=0,
)

st.set_page_config(page_title="Chatbot", layout="centered")

st.title("Conversational AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

prompt = st.chat_input(placeholder="Enter your prompt...")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
    with st.chat_message("assistant"):
        response = llm.invoke(prompt).content
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
    


