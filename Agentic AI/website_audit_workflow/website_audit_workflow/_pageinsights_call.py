import requests
import json

# ---------------------------
# Configuration
# ---------------------------
url_to_analyze = "https://foodsinn.co/"  #   https://lalqila.com  https://alvigha.com/
 
# Helper function to fetch PageSpeed Insights data
def fetch_pagespeed_data(url, strategy="mobile"):
    PAGESPEED_API_KEY = "AIzaSyBEpGSZmVSETUXSHp0UluOqgiN8ETZ4kRw"

    api_url = (
    f"https://www.googleapis.com/pagespeedonline/v5/runPagespeed?"
    f"url={url}"
    f"&key={PAGESPEED_API_KEY}"
    f"&strategy={strategy}"
    "&category=performance"
    "&category=accessibility"
    "&category=best-practices"
    "&category=seo"
)   
    response = requests.get(api_url)
    response.raise_for_status()
    return response.json()

# ---------------------------
# Extract relevant data
# ---------------------------
def extract_audit_data(ps_data):
    lighthouse = ps_data.get("lighthouseResult", {})
    categories = lighthouse.get("categories", {})
    audits = lighthouse.get("audits", {})

    # Scores
    scores = {
        "performance_score": categories["performance"]["score"] * 100,
        "accessibility_score": categories["accessibility"]["score"] * 100,
        "best_practices_score": categories["best-practices"]["score"] * 100,
        "seo_score": categories["seo"]["score"] * 100
    }

    # Core Web Vitals
    core_web_vitals = {}
    vitals = ["first-contentful-paint", "largest-contentful-paint", "speed-index", "total-blocking-time", "cumulative-layout-shift"]
    
    for audit_id in vitals:
        value = audits.get(audit_id, {}).get("displayValue")
        if value:
            core_web_vitals[audit_id] = value

    # Opportunities (top suggestions)
    opportunity_keys = [k for k in audits.keys() if audits[k].get("score") is not None and audits[k].get("score") < 1]
    opportunities = []
    for key in opportunity_keys:
        title = audits[key].get("title")
        if title:
            opportunities.append(title)

    # Diagnostics
    diagnostics = {}
    diag_audits = audits.get("diagnostics", {}).get("details", {}).get("items", [{}])[0]
    if diag_audits:
        diagnostics["requests"] = diag_audits.get("numRequests")
        diagnostics["page_size"] = diag_audits.get("totalByteWeight")
        diagnostics["third_party_scripts"] = diag_audits.get("numScripts", 0)

    return {
        "scores": scores,
        "core_web_vitals": core_web_vitals,
        "opportunities": opportunities,
        "diagnostics": diagnostics
    }

# ---------------------------
# Run Analysis for Mobile and Desktop
# ---------------------------
# _pageinsights_call.py

def run_pagespeed_analysis(url):

    data_mobile = fetch_pagespeed_data(url, strategy="mobile")
    data_desktop = fetch_pagespeed_data(url, strategy="desktop")

    analysis_result = {
        "url": url,
        "mobile": extract_audit_data(data_mobile),
        "desktop": extract_audit_data(data_desktop),
        "total_analysis_time_ms": data_mobile.get("lighthouseResult", {}).get("timing", {}).get("total", 0)
    }

    return analysis_result


if __name__ == "__main__":
    # ---------------------------
    # Print the JSON result
    # ---------------------------
    print(json.dumps(run_pagespeed_analysis(url_to_analyze), indent=2))