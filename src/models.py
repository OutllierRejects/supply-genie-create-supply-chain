from typing import List, Union, Optional
from pydantic import BaseModel, Field


class Supplier(BaseModel):
    company_name: str = Field(description="Name of the company")
    location: str = Field(description="Location of the company")
    rating: float = Field(description="Rating of the company")
    price_range: str = Field(description="Price range of the products")
    lead_time: str = Field(description="Lead time for delivery")
    moq: str = Field(description="Minimum order quantity")
    certifications: List[str] = Field(description="List of certifications")
    specialties: List[str] = Field(description="List of specialties")
    response_time: str = Field(description="Response time")
    contact: Optional[str] = Field(default=None, description="Contact information")


class SupplierSearchIndexQuery(BaseModel):
    price_range: str = Field(description="Price range of the products")
    location: str = Field(description="Location of the company")
    specialties: List[str] = Field(description="List of specialties")
    certifications: List[str] = Field(description="List of certifications")
    lead_time: str = Field(description="Lead time for delivery")

    def build_filter(self) -> dict[str, Union[str, List[str]]]:
        filter = {}
        if self.price_range:
            filter["price_range"] = self.price_range
        if self.location:
            filter["location"] = self.location
        if self.specialties:
            filter["specialties"] = {"$all": self.specialties}
        if self.certifications:
            filter["certifications"] = {"$all": self.certifications}
        if self.lead_time:
            filter["lead_time"] = self.lead_time
        return filter


class AgentConfig(BaseModel):
    query: str = Field(
        description="The query string to search for suppliers.",
        min_length=1,
        max_length=500,
    )
    chat_history: Optional[List[dict]] = Field(
        default=None,
        description="Optional chat history to provide context for the search.",
    )


class SupplierExplorationAgentResponse(BaseModel):
    suppliers: List[Supplier] = Field(
        description="List of suppliers matching the search criteria."
    )


class RequirementAnalysisResponse(BaseModel):
    required_material: str = Field(description="The primary material required.")
    region: Optional[str] = Field(
        default=None, description="The geographical region of interest."
    )
    price_range: Optional[str] = Field(
        default=None, description="Acceptable price range for the material."
    )
    specialties: Optional[List[str]] = Field(
        default=None,
        description="Specific processing or manufacturing specialties required.",
    )
    certifications: Optional[List[str]] = Field(
        default=None, description="Required certifications for suppliers."
    )
    lead_time: Optional[str] = Field(
        default=None, description="Acceptable lead time for delivery."
    )
    additional_details: Optional[str] = Field(
        default=None, description="Any other relevant details or requirements."
    )


class WebSearchQuery(BaseModel):
    query: str = Field(
        description="The query string to search for suppliers.",
        min_length=1,
        max_length=500,
    )


class WebExtractQuery(BaseModel):
    urls: List[str] = Field(
        description="List of URLs to extract supplier information from."
    )
