import streamlit as st


st.set_page_config(page_title="GenAI", layout="centered")
st.title("Hello World")
st.write("Welcome to GenAI, your AI assistant for generating content and answering questions. How can I assist you today?")

st.file_uploader("Upload a file", type=["txt", "pdf", "docx"])
st.text_input("Ask a question or enter a prompt", placeholder="Type your question or prompt here...")

st.image("download.jpg", caption="GenAI Image Placeholder")

if st.button("Analyze Image"):
    st.warning("Image analysis feature is under development. Please check back later.")
    st.spinner("Spinning up the AI engine...")
