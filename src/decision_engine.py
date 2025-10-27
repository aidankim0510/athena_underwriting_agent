import math
from .schemas import Application, Policy, Decision

def compute_dti(annual_income: float, monthly_debt: float) -> float:
    return (monthly_debt * 12 / annual_income) * 100 if annual_income > 0 else math.inf

def classify_risk(score: int) -> str:
    if score >= 720: return "low"
    if 650 <= score <= 719: return "medium"
    return "high"

def score_range(risk: str) -> str:
    if risk == "low":
        return "≥ 720"
    elif risk == "medium":
        return "650-719"
    return "< 650"


def evaluate(app: Application, policy: Policy) -> Decision:
    cs, inc, debt, months = app.creditScore, app.annualIncome, app.monthlyDebt, app.employmentMonths
    first_time, self_emp = app.isFirstTimeBuyer, app.isSelfEmployed
    applied = []
    risk = classify_risk(cs)

    # Automatic denials
    if cs < policy.auto_deny_credit:
        applied.append(f"Automatic denial: credit score {cs} < {policy.auto_deny_credit}.")
        reasoning = (
            f"Credit score {cs} falls in high-risk category ({score_range('high')})\n"
            f"Debt-to-income ratio: N/A (auto-deny on credit)\n"
            f"Employment: {months} months"
        )
        return Decision(decision="denied", reasoning=reasoning, riskLevel="high", appliedRules=applied)

    if inc < policy.income_min:
        applied.append(f"Automatic denial: income ${inc:,.0f} < minimum ${policy.income_min:,.0f}.")
        reasoning = (
            f"Credit score {cs} falls in {risk}-risk category ({score_range(risk)})\n"
            f"Debt-to-income ratio: N/A (auto-deny on income)\n"
            f"Employment: {months} months"
        )
        return Decision(decision="denied", reasoning=reasoning, riskLevel=risk, appliedRules=applied)

    # Employment requirement
    tier = policy.tiers[risk]
    required_months = policy.self_employed_months if self_emp else tier.employment_months
    if months < required_months:
        applied.append(f"Employment {months} months < required {required_months}.")
        reasoning = (
            f"Credit score {cs} falls in {risk}-risk category ({score_range(risk)})\n"
            f"Debt-to-income ratio: N/A (denied due to employment tenure)\n"
            f"Employment: {months} months (below required {required_months} months)"
        )
        return Decision(decision="denied", reasoning=reasoning, riskLevel=risk, appliedRules=applied)

    # DTI and first-time buyer leniency
    dti = compute_dti(inc, debt)
    leniency = policy.first_time_buyer_leniency if first_time else 0.0
    allowed = (tier.dti_limit or 0.0) + leniency

    applied.append(f"Credit score {cs} → {risk}-risk; DTI limit {allowed:.1f}%.")
    applied.append(f"Applicant DTI {dti:.1f}%.")

    # Determine decision
    decision = "denied"
    if risk in ("low", "medium") and dti <= allowed:
        decision = "approved"
    elif risk == "high" and tier.income_override and inc > tier.income_override and dti <= (tier.dti_limit or 25.0):
        decision = "approved"
        applied.append("High-risk override satisfied.")

    # Build multiline reasoning
    limit_phrase = (
        f"(within {allowed:.1f}% limit for {risk}-risk)"
        if dti <= allowed else
        f"(exceeds {allowed:.1f}% limit for {risk}-risk)"
    )
    emp_phrase = (
        f"(meets {required_months}-month minimum)"
        if months >= required_months else
        f"(below required {required_months} months)"
    )

    reasoning = (
        f"Credit score {cs} falls in {risk}-risk category ({score_range(risk)})\n"
        f"Debt-to-income ratio: {dti:.1f}% {limit_phrase}\n"
        f"Employment: {months} months {emp_phrase}"
    )

    return Decision(
        decision=decision,
        reasoning=reasoning,
        riskLevel=risk,
        appliedRules=applied
    )