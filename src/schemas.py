from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict

DecisionT = Literal["approved", "denied"]
RiskT = Literal["low", "medium", "high"]

class Application(BaseModel):
    applicantId: str
    requestedAmount: float
    annualIncome: float
    monthlyDebt: float
    creditScore: int
    employmentMonths: int
    isFirstTimeBuyer: bool = False
    isSelfEmployed: bool = False

class PolicyTier(BaseModel):
    risk: RiskT
    dti_limit: Optional[float] = None
    employment_months: int
    income_override: Optional[int] = None

class Policy(BaseModel):
    tiers: Dict[RiskT, PolicyTier]
    income_min: int = 35000
    auto_deny_credit: int = 600
    auto_deny_dti_excess: int = 5
    first_time_buyer_leniency: float = 5.0
    self_employed_months: int = 24

class Decision(BaseModel):
    decision: DecisionT
    reasoning: str
    riskLevel: RiskT
    appliedRules: List[str] = Field(default_factory=list)