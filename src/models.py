from typing import List, Union, Optional
from typing_extensions import TypedDict, NotRequired

from pydantic import BaseModel, Field, HttpUrl


class CreateChainState(TypedDict):
    session_id: str
    raw_input: dict
    esg_preference: NotRequired[str]
    suppliers: list
    exploration_results: list
    evaluation_feedback: str
    final_report: dict
    retry_count: NotRequired[int]


class Supplier(BaseModel):
    name: str
    score: float
    reasons: str
    price: float
    currency: Optional[str]
    unit: Optional[str]
    delivery_time: str
    url: Optional[HttpUrl]


class SuccessReport(BaseModel):
    status: str = Field("success", const=True)
    top_suppliers: List[Supplier] = Field(..., min_items=1)
    evaluation_feedback: str
    evaluation_model: str


class FailureReport(BaseModel):
    status: str = Field("failed", const=True)
    message: str


FinalReport = Union[SuccessReport, FailureReport]

# Tools Configuration

