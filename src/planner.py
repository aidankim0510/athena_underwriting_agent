from typing import Tuple, List
from .schemas import Application, Policy, Decision
from .policy_extractor import parse_policy_from_pdf
from .decision_engine import evaluate

def run_agent(policy_pdf: str, app: Application) -> Tuple[Decision, List[tuple]]:
    trace: List[tuple] = []
    policy: Policy = parse_policy_from_pdf(policy_pdf)
    trace.append(("parse_policy", "Parsed policy with Gemini (fallback=DEFAULT_POLICY if needed)"))
    decision: Decision = evaluate(app, policy)
    trace.append(("evaluate", f"risk={decision.riskLevel}, decision={decision.decision}"))
    return decision, trace