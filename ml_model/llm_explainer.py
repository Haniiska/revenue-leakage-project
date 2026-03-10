import requests


def explain_issue(claim_id, issue, billed, paid):

    prompt = f"""
    Claim ID: {claim_id}
    Issue: {issue}
    Billed Amount: {billed}
    Paid Amount: {paid}

    Explain the healthcare revenue leakage reason in simple terms.
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()

    return result["response"]