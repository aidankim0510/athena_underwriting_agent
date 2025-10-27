import argparse, json
from dotenv import load_dotenv
from .schemas import Application
from .planner import run_agent


def main():
    load_dotenv()
    p = argparse.ArgumentParser(description="Underwriting Agent (Gemini-first)")
    p.add_argument("--policy", required=True, help="Path to loan_policy.pdf")
    p.add_argument("--app", required=True, help="Path to application JSON")
    args = p.parse_args()

    # Load and validate the application JSON
    with open(args.app) as f:
        app = Application.model_validate_json(f.read())

    # Run the underwriting agent
    decision, trace = run_agent(args.policy, app)

    print("\n================= Underwriting Decision =================")
    print(f"Decision:   {decision.decision.upper()}")
    print(f"Risk Level: {decision.riskLevel.capitalize()}\n")

    # print reasoning with real newlines
    print("Reasoning:")
    print(decision.reasoning.replace("\\n", "\n"))

    # print applied rules nicely
    if getattr(decision, "appliedRules", []):
        print("\nApplied Rules:")
        for rule in decision.appliedRules:
            print(" - " + rule.replace("\\u2192", "→"))

    print("==========================================================\n")

    print("\nTRACE:")
    for step, detail in trace:
        print(f"- {step}: {detail}")


if __name__ == "__main__":
    main()