from fastapi import APIRouter, HTTPException, File, UploadFile
from app.ai.schemas import (
    IngredientAnalysisRequest, 
    AnalysisResponse,
    DecisionRequest,
    DecisionEngineResponse
)
from app.ai.service import ai_service
from app.ai.coordinator import coordinator

router = APIRouter(prefix="/analyze", tags=["AI Analysis"])

@router.post("/text", response_model=AnalysisResponse)
async def analyze_ingredients_text(request: IngredientAnalysisRequest):
    """Legacy endpoint for backward compatibility"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
        
    result = await ai_service.analyze_text(request.text)
    return result

@router.post("/image", response_model=AnalysisResponse)
async def analyze_ingredients_image(file: UploadFile = File(...)):
    """Legacy endpoint for backward compatibility"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
        
    try:
        contents = await file.read()
        result = await ai_service.analyze_image(contents, file.content_type)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/decision", response_model=DecisionEngineResponse)
async def analyze_decision(request: DecisionRequest):
    """
    New transparent decision engine endpoint.
    Uses multi-agent coordination:
    1. Intent Classification
    2. Ingredient Interpretation (structured signals)
    3. Rule-based Decision Engine
    4. Consumer Explanation
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        result = await coordinator.process(request)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Decision engine error: {str(e)}")
