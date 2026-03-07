# import streamlit as st
# from langchain_groq import ChatGroq
# from langchain_core.prompts import PromptTemplate
# from dotenv import load_dotenv
# import os

# # Load environment variables
# load_dotenv()

# # Prompt template
# template = """
# You are a senior corporate strategy analyst.

# Write a professional executive-level strategic article.

# Topic: {topic}

# Tone: {tone}

# The article should include:
# 1. Executive Summary
# 2. Strategic Analysis
# 3. Industry Impact
# 4. Future Outlook
# 5. Key Takeaways

# Write clearly for executives and business leaders.
# """

# prompt = PromptTemplate(
#     input_variables=["topic", "tone"],
#     template=template
# )

# model = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0,
# )

# # ------------------------
# # Streamlit UI
# # ------------------------

# st.set_page_config(page_title="Executive Strategy Article Generator")

# st.title("Executive Strategic Article Generator")

# st.write("Generate executive-level strategic articles for corporate leadership.")

# topic = st.text_input("Enter Article Topic")

# tone = st.selectbox(
#     "Select Tone",
#     ["Formal", "Concise", "Strategic"]
# )

# if st.button("Generate Article"):
#     with st.spinner("Generating article..."):
#         article = model.invoke(prompt.format(topic=topic, tone=tone))
#         st.subheader("Generated Article")
#         st.write(article)


import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Prompt template
template = """
You are a senior corporate strategy analyst.

Write a professional executive-level strategic article.

Topic: {topic}

Tone: {tone}

The article should include:
1. Executive Summary
2. Strategic Analysis
3. Industry Impact
4. Future Outlook
5. Key Takeaways

Write clearly for executives and business leaders.
"""

prompt = PromptTemplate(
    input_variables=["topic", "tone"],
    template=template
)

model = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)

st.set_page_config(page_title="Executive Strategy Article Generator", layout="wide")

st.title("Executive Strategic Article Generator")

# Create two columns
col1, col2 = st.columns(2)

# LEFT COLUMN → INPUT
with col1:
    st.header("Input")

    topic = st.text_input("Enter Article Topic")

    tone = st.selectbox(
        "Select Tone",
        ["Formal", "Concise", "Strategic"]
    )

    generate = st.button("Generate Article")


# RIGHT COLUMN → OUTPUT
with col2:
    st.header("Generated Article")

    if generate:
        with st.spinner("Generating article..."):
            article = model.invoke(prompt.format(topic=topic, tone=tone))
            st.write(article.content)