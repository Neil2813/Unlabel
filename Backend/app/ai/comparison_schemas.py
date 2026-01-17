"""
Comparison Schemas for comparing multiple products
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from app.ai.schemas import DecisionEngineResponse


class ComparisonRequest(BaseModel):
    """Request to compare two products"""
    product_a_text: str = Field(..., description="Ingredient/nutrition text for Product A")
    product_b_text: str = Field(..., description="Ingredient/nutrition text for Product B")
    product_a_name: Optional[str] = Field(None, description="Optional name for Product A")
    product_b_name: Optional[str] = Field(None, description="Optional name for Product B")


class ComparisonInsight(BaseModel):
    """High-level comparison insight"""
    winner: str = Field(..., description="Which product is better overall: 'A', 'B', or 'Similar'")
    summary: str = Field(..., description="One-sentence comparison summary")
    key_differences: List[str] = Field(..., description="Top 3 key differences")


class ComparisonResponse(BaseModel):
    """Response comparing two products"""
    product_a_name: str
    product_b_name: str
    product_a_analysis: DecisionEngineResponse
    product_b_analysis: DecisionEngineResponse
    comparison_insight: ComparisonInsight
    recommendation: str = Field(..., description="Recommendation based on comparison")
