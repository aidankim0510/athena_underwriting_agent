import os, json
from typing import Optional, Dict, Any
import google.generativeai as genai
from tenacity import retry, wait_exponential, stop_after_attempt

PROMPT = """You are parsing a lending policy into structured JSON.
Return ONLY a JSON object with this exact structure (no prose, no markdown):

{{
  "tiers": {{
    "low":    {{"dti_limit": 40, "employment_months": 12, "income_override": null}},
    "medium": {{"dti_limit": 30, "employment_months": 18, "income_override": null}},
    "high":   {{"dti_limit": 25, "employment_months": 24, "income_override": 150000}}
  }},
  "income_min": 35000,
  "auto_deny_credit": 600,
  "auto_deny_dti_excess": 5,
  "first_time_buyer_leniency": 5.0,
  "self_employed_months": 24
}}

Fill numeric values using the policy text exactly. If high-risk has a special income override, set it; otherwise null.

POLICY TEXT:
---
{policy_text}
---
"""

def _parse_json_block(text: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(text)
    except Exception:
        s, e = text.find("{"), text.rfind("}")
        if s != -1 and e != -1:
            try:
                return json.loads(text[s:e+1])
            except Exception:
                return None
        return None

@retry(wait=wait_exponential(min=1, max=8), stop=stop_after_attempt(3))
def parse_policy_with_gemini(policy_text: str) -> Optional[Dict[str, Any]]:
    """Ask Gemini to structure the policy text as JSON."""
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY environment variable.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)
    response = model.generate_content(PROMPT.format(policy_text=policy_text))
    content = response.text or ""
    return _parse_json_block(content)