from typing import List
from pydantic import BaseModel, Field


class Discrepancy(BaseModel):
    field: str = Field(..., description="The field in which the discrepancy occurs")
    cv_value: str = Field(..., description="The value found in the CV")
    linkedin_value: str = Field(..., description="The value found in the LinkedIn profile")
    issue: str = Field(..., description="Description of the issue or mismatch")


class FinalDecisionOutput(BaseModel):
    verdict: str = Field(..., description="Select or Reject")
    justification: str = Field(..., description="Detailed reasoning based on analysis")
    confidence_score: int = Field(..., description="Numeric confidence score from CV analysis (0-100)")
    matching_score: int = Field(..., description="Numeric matching score between CV and job description (0-100)")
    discrepancies: List[Discrepancy] = Field(
        default_factory=list,
        description="List of discrepancies found between CV and LinkedIn"
    )