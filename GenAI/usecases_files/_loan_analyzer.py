# from pydantic import BaseModel, Field
# from dotenv import load_dotenv
# from langchain_groq import ChatGroq
# import json

# load_dotenv()

# class LoanRiskOutput(BaseModel):
#     risk_level: str = Field(..., description="Risk level: Low, Medium, High")
#     risk_score: int = Field(..., description="Numeric risk score 0-100")
#     recommended_action: str = Field(..., description="Action: Approve, Manual Review, Reject")
#     suggested_interest_rate: float = Field(..., description="Interest rate to assign based on risk")
#     income_stability: str = Field(..., description="Income stability: Low, Medium, High")
#     creditworthiness: str = Field(..., description="Overall creditworthiness: Poor, Moderate, Strong")

# llm = ChatGroq(
#     model="llama-3.1-8b-instant",
#     temperature=0,
# )

# structured_llm = llm.with_structured_output(LoanRiskOutput)


# applicant_data = """
# Applicant Name: Ahmed Khan
# Income:
# - Monthly Gross: PKR 420,000
# - Monthly Net: PKR 360,000
# - Freelance Income: PKR 40,000
# Employment:
# - Current Employer: TechNova Solutions Pvt. Ltd.
# - Role: Senior Software Engineer
# - Total Experience: 10 years
# Credit:
# - Credit Score: 720
# - Credit Cards: 2 (Total Limit PKR 1,000,000)
# - Credit Utilization: 32%
# - Existing Car Loan: PKR 650,000, EMI PKR 45,000
# """

# output = structured_llm.invoke(applicant_data)
# # .model_dump() converts pydantic object to python dict
# # .dumps() used for json output
# print(json.dumps(output.model_dump(), indent=4))




import streamlit as st
from PyPDF2 import PdfReader
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# Load environment variables
load_dotenv()

# --- Define structured output model ---
class LoanRiskOutput(BaseModel):
    risk_level: str = Field(..., description="Risk level: Low, Medium, High")
    risk_score: int = Field(..., description="Numeric risk score 0-100")
    recommended_action: str = Field(..., description="Action: Approve, Manual Review, Reject")
    suggested_interest_rate: float = Field(..., description="Interest rate to assign based on risk")
    income_stability: str = Field(..., description="Income stability: Low, Medium, High")
    creditworthiness: str = Field(..., description="Overall creditworthiness: Poor, Moderate, Strong")

# --- Initialize LLM ---
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
)
structured_llm = llm.with_structured_output(LoanRiskOutput)

# --- Streamlit App ---
st.title("AI Loan Application Risk Analyzer (PDF Upload)")
st.markdown("""
Upload a PDF of a loan application. The app will extract text and generate a **structured risk assessment** using AI.
""")

# PDF Upload
uploaded_file = st.file_uploader("Upload Loan Application PDF", type="pdf")

if uploaded_file:
    # --- Extract text from PDF ---
    reader = PdfReader(uploaded_file)
    pdf_text = "\n".join(page.extract_text() for page in reader.pages)

    st.subheader("Extracted PDF Text (Preview)")
    st.text_area("PDF Text Preview", pdf_text[:1000], height=200)

    if st.button("Analyze Loan Risk"):
        with st.spinner("Processing with AI..."):
            # Pass extracted text to structured LLM
            output = structured_llm.invoke(pdf_text)
            result = output.model_dump()

            # --- Display key indicators nicely ---
            st.subheader("Key Risk Indicators")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Risk Level", result["risk_level"])
            col2.metric("Risk Score", result["risk_score"])
            col3.metric("Recommended Action", result["recommended_action"])

            st.subheader("Financial Details")
            col4, col5 = st.columns(2)
            col4.metric("Suggested Interest Rate (%)", result["suggested_interest_rate"])
            col5.metric("Income Stability", result["income_stability"])

            st.subheader("Creditworthiness")
            st.info(result["creditworthiness"])

            # Optional: Expandable raw JSON
            with st.expander("Show Raw JSON Output"):
                st.json(result)