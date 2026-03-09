from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage
from langchain_groq import ChatGroq
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

llm = ChatGroq(
   model="llama-3.1-8b-instant",
   temperature=0 
)
template = ChatPromptTemplate([
    ("system", "You are a fitness expert. Give practical and safe fitness advice."),
    ("placeholder", "{conversation}"),
    ("human", "{question}")
])

st.title("Fitness Chatbot 💪")
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

user_input = st.chat_input("Enter your query")

if user_input:

    with st.chat_message("user"):
        st.write(user_input)

    prompt = template.invoke({
        "conversation": st.session_state.messages,
        "question": user_input
    })

    with st.chat_message("assistant"):
        result = llm.stream(prompt)
        ai_response = st.write_stream(result)        
    
    st.session_state.messages.append(HumanMessage(content=user_input))
    st.session_state.messages.append(AIMessage(content=ai_response))


