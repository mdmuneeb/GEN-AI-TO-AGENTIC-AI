import streamlit as st
from assistant import execute_workflow
from langchain_core.messages import HumanMessage, AIMessage

result = execute_workflow("How many loyalty points do I have and what is my tier")
print(result)


st.set_page_config(page_title="AI Assistant", layout="centered")

st.title("Imtiaz Superstore AI Assistant")


if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display previous chat history ---
for msg in st.session_state.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.write(msg.content)

# -----------------------------
# User Query Input
# -----------------------------
user_input = st.chat_input("Enter your query")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    response = execute_workflow(user_input)
    with st.chat_message("assistant"):
        result = execute_workflow(user_input)
        st.write(result)  

    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.messages.append(AIMessage(content=result))