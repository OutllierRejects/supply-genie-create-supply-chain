# models.py
from typing import List, Literal, Union
from pydantic import BaseModel, HttpUrl, Field

class Supplier(BaseModel):
    name: str
    score: float
    reasons: List[str]
    warnings: List[str]
    url: HttpUrl

class SuccessReport(BaseModel):
    status: Literal["success"]
    summary: str
    top_suppliers: List[Supplier] = Field(..., min_items=1)
    evaluation_model: str
    evaluation_notes: str

class FailureReport(BaseModel):
    status: Literal["failed"]
    message: str

FinalReport = Union[SuccessReport, FailureReport]
