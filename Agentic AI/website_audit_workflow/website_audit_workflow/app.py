# app.py
import streamlit as st
from _parallel_workflow import graph

st.set_page_config(
    page_title="Website Audit Tool",
    page_icon="🌐",
    layout="wide"
)

st.title("🌐 Website Audit Tool")
st.markdown(
    """
    Enter the website URL below and run the audit. 
    The tool will analyze performance, SEO, UX, and provide a professional audit report.
    """
)

# -------------------------
# URL Input
# -------------------------
url_input = st.text_input("Enter website URL")

if st.button("Run Audit"):
    if not url_input.strip():
        st.warning("Please enter a valid URL!")
    else:
        with st.spinner("Running website audit, please wait..."):
            try:
                # Call your LangGraph workflow
                result = graph.invoke({"url": url_input.strip()})
                report = result.get("final_report", "No report generated.")
                
                # -------------------------
                # Display Results
                # -------------------------
                st.subheader("📄 Audit Report")
                st.markdown(report)

                # Optional: Display structured page data
                page_data = result.get("page_data", {})
                if page_data:
                    st.subheader("📊 Page Data (Structured)")
                    st.json(page_data)

            except Exception as e:
                st.error(f"Error running audit: {e}")