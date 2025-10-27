from .utils.pdf import extract_text
from .llm_parser import parse_policy_with_gemini
from .schemas import Policy, PolicyTier

DEFAULT_POLICY = Policy(
    tiers={
        "low":    PolicyTier(risk="low", dti_limit=40.0, employment_months=12, income_override=None),
        "medium": PolicyTier(risk="medium", dti_limit=30.0, employment_months=18, income_override=None),
        "high":   PolicyTier(risk="high", dti_limit=25.0, employment_months=24, income_override=150000),
    },
    income_min=35000,
    auto_deny_credit=600,
    auto_deny_dti_excess=5,
    first_time_buyer_leniency=5.0,
    self_employed_months=24,
)

def parse_policy_from_pdf(path: str) -> Policy:
    raw = extract_text(path)
    data = parse_policy_with_gemini(raw)
    if not data:
        return DEFAULT_POLICY

    tiers = data.get("tiers", {})
    def tier(name, risk, emp_default):
        d = tiers.get(name, {}) or {}
        return PolicyTier(
            risk=risk,
            dti_limit=d.get("dti_limit"),
            employment_months=int(d.get("employment_months", emp_default)),
            income_override=d.get("income_override"),
        )
    return Policy(
        tiers={
            "low": tier("low", "low", 12),
            "medium": tier("medium", "medium", 18),
            "high": tier("high", "high", 24),
        },
        income_min=int(data.get("income_min", 35000)),
        auto_deny_credit=int(data.get("auto_deny_credit", 600)),
        auto_deny_dti_excess=int(data.get("auto_deny_dti_excess", 5)),
        first_time_buyer_leniency=float(data.get("first_time_buyer_leniency", 5.0)),
        self_employed_months=int(data.get("self_employed_months", 24)),
    )