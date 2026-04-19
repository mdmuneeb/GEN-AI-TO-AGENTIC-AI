from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from _pageinsights_call import run_pagespeed_analysis
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
   model="llama-3.1-8b-instant",
   temperature=0 
)

# -------------------------
# State
# -------------------------

class AuditState(TypedDict):
    url: str
    page_data: dict
    performance_analysis: str
    prioritized_issues: str
    client_summary: str
    recommendations: str
    final_report: str


# -------------------------
# Url Intake
# -------------------------

def url_intake(state: AuditState):

    url = state["url"].strip()

    if not url.startswith("http"):
        url = "https://" + url

    return {"url": url}


# -------------------------
# PageSpeed Analyzer
# -------------------------

def pagespeed_analyzer(state: AuditState):

    url = state["url"]

    page_data = run_pagespeed_analysis(url)

    return {"page_data": page_data}


# -------------------------
# Performance Analyzer
# -------------------------

def performance_analyzer(state: AuditState):

    prompt = ChatPromptTemplate.from_template(
        """
        Analyze these website performance metrics.

        Metrics:
        {data}

        Identify key performance problems and explain their impact.
        """
    )

    chain = prompt | llm | StrOutputParser()

    analysis = chain.invoke({"data": state["page_data"]})

    return {"performance_analysis": analysis}


# -------------------------
# Issue Prioritizer
# -------------------------

def issue_prioritizer(state: AuditState):

    prompt = ChatPromptTemplate.from_template(
        """
        From the following analysis identify the top 3-5 issues.

        Prioritize based on:
        - Business impact
        - SEO impact
        - User experience

        Analysis:
        {analysis}
        """
    )

    chain = prompt | llm | StrOutputParser()

    issues = chain.invoke({"analysis": state["performance_analysis"]})

    return {"prioritized_issues": issues}

# -------------------------
# Audit Summary
# -------------------------

def audit_summary_generator(state: AuditState):

    prompt = ChatPromptTemplate.from_template(
        """
        You are an expert website auditor.

        Using the following prioritized issues, write a concise
        WEBSITE AUDIT SUMMARY suitable for a professional report.

        The summary should:
        - Explain overall website health
        - Mention performance concerns
        - Mention potential SEO and UX impact
        - Be written in a professional consulting tone

        Issues:
        {issues}
        """
    )

    chain = prompt | llm | StrOutputParser()

    summary = chain.invoke({"issues": state["prioritized_issues"]})

    return {"client_summary": summary}

# -------------------------
# Action Recommender
# -------------------------

def action_recommender(state: AuditState):

    prompt = ChatPromptTemplate.from_template(
        """
        Suggest practical fixes for these website issues.

        Provide effort level:
        Low / Medium / High

        Issues:
        {issues}
        """
    )

    chain = prompt | llm | StrOutputParser()

    actions = chain.invoke({"issues": state["prioritized_issues"]})

    return {"recommendations": actions}

# -------------------------
# Final Audit Report
# -------------------------

def final_report(state: AuditState):

    prompt = ChatPromptTemplate.from_template(
        """
        You are a professional website performance consultant.

        Create a structured WEBSITE AUDIT REPORT.

        The report must contain the following sections:

        1. Executive Summary
        Overview of the website performance and health.

        2. Key Performance Issues
        List the main problems identified.

        3. Business Impact
        Explain how these issues affect:
        - User experience
        - Conversion rates
        - SEO rankings
        - Page speed

        4. Recommended Fixes
        Provide actionable recommendations.

        Audit Summary:
        {summary}

        Recommendations:
        {recommendations}

        Format the report professionally using clear headings.
        """
    )

    chain = prompt | llm | StrOutputParser()

    report = chain.invoke({
        "summary": state["client_summary"],
        "recommendations": state["recommendations"]
    })

    return {"final_report": report}


# -------------------------
# Build Graph
# -------------------------

builder = StateGraph(AuditState)

builder.add_node("UrlIntake", url_intake)
builder.add_node("PageInsightsAnalyzer", pagespeed_analyzer)
builder.add_node("PerformanceAnalyzer", performance_analyzer)
builder.add_node("IssuePrioritizer", issue_prioritizer)
builder.add_node("AuditSummaryGenerator", audit_summary_generator)
builder.add_node("ActionRecommender", action_recommender)
builder.add_node("FinalReport", final_report)


builder.add_edge(START, "UrlIntake")
builder.add_edge("UrlIntake", "PageInsightsAnalyzer")
builder.add_edge("PageInsightsAnalyzer", "PerformanceAnalyzer")
builder.add_edge("PerformanceAnalyzer", "IssuePrioritizer")
builder.add_edge("IssuePrioritizer", "AuditSummaryGenerator")
builder.add_edge("AuditSummaryGenerator", "ActionRecommender")
builder.add_edge("ActionRecommender", "FinalReport")
builder.add_edge("FinalReport", END)


graph = builder.compile()

# Visualization
# print(graph.get_graph().print_ascii())
# print(graph.get_graph().draw_mermaid())




if __name__ == "__main__":
    # # -------------------------
    # # Run Workflow
    # # -------------------------

    result = graph.invoke({
        "url": "https://lalqila.com/"
    })

    print(result["final_report"])








