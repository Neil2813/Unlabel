from fastapi import APIRouter, HTTPException, File, UploadFile, Query
from app.ai.schemas import (
    IngredientAnalysisRequest, 
    AnalysisResponse,
    DecisionRequest,
    DecisionEngineResponse
)
from app.ai.comparison_schemas import ComparisonRequest, ComparisonResponse
from app.ai.service import ai_service
from app.ai.coordinator import coordinator
from app.ai.autonomous_agent import autonomous_agent
from app.ai.comparison_service import comparison_service

router = APIRouter(prefix="/analyze", tags=["AI Analysis"])

# ============================================================================
# AUTONOMOUS AGENT ENDPOINTS (Multi-step orchestration)
# ============================================================================

@router.post("/autonomous/image")
async def autonomous_analyze_image(
    file: UploadFile = File(...),
    user_query: str = Query(None, description="Optional user query for context")
):
    """
    🤖 AUTONOMOUS AI AGENT - Image Analysis
    
    This endpoint orchestrates a multi-step autonomous workflow:
    1. Analyzes image to extract summary and key takeaways
    2. Autonomously decides next steps based on initial analysis
    3. Executes follow-up actions (decision engine, product search, etc.)
    4. Synthesizes all information into comprehensive response
    
    The agent acts autonomously, making intelligent decisions about what
    information would be most valuable to the user.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        result = await autonomous_agent.analyze_autonomously(
            image_data=contents,
            user_query=user_query
        )
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Autonomous agent error: {str(e)}")


@router.post("/autonomous/text")
async def autonomous_analyze_text(
    text: str = Query(..., description="Ingredient text or product information"),
    user_query: str = Query(None, description="Optional user query for context")
):
    """
    🤖 AUTONOMOUS AI AGENT - Text Analysis
    
    This endpoint orchestrates a multi-step autonomous workflow:
    1. Analyzes text to extract summary and key takeaways
    2. Autonomously decides next steps based on initial analysis
    3. Executes follow-up actions (decision engine, product search, etc.)
    4. Synthesizes all information into comprehensive response
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        result = await autonomous_agent.analyze_autonomously(
            text_data=text,
            user_query=user_query
        )
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Autonomous agent error: {str(e)}")

# ============================================================================
# COMPARISON ENDPOINT (Compare two products side-by-side)
# ============================================================================

@router.post("/compare", response_model=ComparisonResponse)
async def compare_products(request: ComparisonRequest):
    """
    🔬 PRODUCT COMPARISON
    
    Compare two products side-by-side:
    - Analyzes both products in parallel using decision engine
    - Highlights key differences
    - Provides clear recommendation
    - Returns full analysis for each product
    """
    if not request.product_a_text.strip() or not request.product_b_text.strip():
        raise HTTPException(status_code=400, detail="Both product texts must be provided")
    
    try:
        result = await comparison_service.compare_products(request)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")

# ============================================================================
# Decision engine endpoints (more specific routes first)
# ============================================================================
@router.post("/decision/image", response_model=DecisionEngineResponse)
async def analyze_decision_image(
    file: UploadFile = File(...),
    conversation_context: str = Query(None, description="Previous conversation context for follow-up queries")
):
    """
    Decision engine endpoint for image input.
    Extracts ingredient/nutrition info from image, then processes through decision engine.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        import google.generativeai as genai
        import PIL.Image
        import io
        from config.settings import GEMINI_API_KEY
        
        if not GEMINI_API_KEY:
            raise HTTPException(status_code=500, detail="AI service not configured")
        
        # Read image
        contents = await file.read()
        image = PIL.Image.open(io.BytesIO(contents))
        
        # Extract text from image using Gemini Vision
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        extraction_prompt = """Extract all ingredient and nutrition information from this food label image.

Return ONLY the following information in a clear, structured format:
1. Ingredients list (if visible)
2. Nutrition facts (if visible) - include all values like calories, carbs, sugars, protein, fiber, fat, etc.
3. Any other relevant product information

Format your response as:
INGREDIENTS:
[list all ingredients]

NUTRITION FACTS:
[all nutrition information]

If any information is unclear or missing, note that in your response."""
        
        import asyncio
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: model.generate_content([extraction_prompt, image])
        )
        
        extracted_text = response.text.strip()
        
        # Create DecisionRequest with extracted text
        decision_request = DecisionRequest(text=extracted_text, conversation_context=conversation_context)
        
        # Process through decision engine
        result = await coordinator.process(decision_request, conversation_context=conversation_context)
        return result
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Decision engine image processing error: {str(e)}")

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
        result = await coordinator.process(request, conversation_context=request.conversation_context)
        return result
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Decision engine error: {str(e)}")

# Legacy endpoints have been removed.
# Use /autonomous/text, /autonomous/image, or /decision instead.