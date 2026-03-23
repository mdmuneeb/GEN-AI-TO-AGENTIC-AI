# drug_ai_app.py
import streamlit as st
import os
import json
import re
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.1-8b-instant"


def read_file(file):
    if file.type == "text/plain":
        return str(file.read(), "utf-8")
    elif file.type == "application/pdf":
        import PyPDF2
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    else:
        return ""

extract_prompt = PromptTemplate(
    input_variables=["text"],
    template="""
You are a pharmaceutical AI assistant. Extract the following from the given drug report:
- Drug Name (generic and alternative)
- Active Ingredients
- Indications
- Dosage Information
- Side Effects
- Contraindications

Return the output as a **valid JSON only**, without any extra text.

JSON keys: drug_name, active_ingredients, indications, dosage, side_effects, contraindications, summary

Drug Report:
{text}
"""
)

llm = ChatGroq(
    model_name=MODEL_NAME,
    groq_api_key=GROQ_API_KEY,
    temperature=0
)

st.set_page_config(page_title="Pharma AI Extraction", layout="wide")
st.title("AI-Powered Pharmaceutical Drug Information Extraction")

uploaded_file = st.file_uploader("Upload a drug report (.txt or .pdf)", type=["txt", "pdf"])

if uploaded_file is not None:
    st.info("Reading file...")
    text = read_file(uploaded_file)

    if not text.strip():
        st.error("Could not read the file. Please upload a valid .txt or .pdf file.")
    else:
        st.success("File loaded successfully! Running AI analysis...")
        try:
            prompt_text = extract_prompt.format(text=text)
            result = llm.invoke(prompt_text)

            st.write("Raw AI output:", result.content)

            match = re.search(r'\{.*\}', result.content, re.DOTALL)
            if match:
                data = json.loads(match.group(0))
            else:
                st.error("AI did not return valid JSON.")
                data = {}

            if data:
                st.subheader("Extracted Drug Information")

                drug_name = data.get("drug_name", {})
                st.markdown(f"**Drug Name (Generic):** {drug_name.get('generic','N/A')}")
                st.markdown(f"**Drug Name (Alternative):** {drug_name.get('alternative','N/A')}")

                st.markdown(f"**Active Ingredients:** {', '.join(data.get('active_ingredients', []))}")

                st.markdown(f"**Indications:** {', '.join(data.get('indications', []))}")

                dosage = data.get("dosage", {})
                adult = dosage.get("adult", {})
                pediatric = dosage.get("pediatric", {})
                st.markdown("**Dosage Information:**")
                st.markdown(f"- Adult: {adult.get('dosage','Not provided')} (Max: {adult.get('max_dose','Not provided')})")
                st.markdown(f"- Pediatric: {pediatric.get('dosage','Not provided')}")

                st.markdown(f"**Side Effects:** {', '.join(data.get('side_effects', []))}")

                st.markdown(f"**Contraindications:** {', '.join(data.get('contraindications', []))}")

                st.subheader("AI-Generated Summary")
                st.write(data.get("summary", "No summary provided."))

        except Exception as e:
            st.error(f"Error during AI analysis: {e}")