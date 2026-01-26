from fastapi import APIRouter, HTTPException, File, UploadFile, Query
from fastapi.responses import StreamingResponse
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
import json
import asyncio

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
    AUTONOMOUS AI AGENT - Image Analysis
    
    This endpoint orchestrates a multi-step autonomous workflow:
    1. Analyzes image to extract summary and key takeaways
    2. Autonomously decides next steps based on initial analysis
    3. Executes follow-up actions (decision engine, product search, etc.
    4. Synthesizes all information into comprehensive response
    
    The agent acts autonomously, making intelligent decisions about what
    information would be most valuable to the user.
    """
    import traceback
    import sys
    
    print(f"📸 Autonomous image analysis request received")
    print(f"   File: {file.filename}, Content-Type: {file.content_type}")
    print(f"   User query: {user_query}")
    
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        contents = await file.read()
        print(f"   Image size: {len(contents)} bytes")
        
        # Check if autonomous_agent is properly initialized
        if not hasattr(autonomous_agent, 'model') or autonomous_agent.model is None:
            error_msg = "Autonomous agent not initialized. Check API key configuration."
            print(f"❌ ERROR: {error_msg}")
            print(f"   - Has model attr: {hasattr(autonomous_agent, 'model')}")
            if hasattr(autonomous_agent, 'model'):
                print(f"   - Model is None: {autonomous_agent.model is None}")
            raise HTTPException(status_code=500, detail=error_msg)
        
        print(f"✅ Autonomous agent model is initialized")
        result = await autonomous_agent.analyze_autonomously(
            image_data=contents,
            user_query=user_query
        )
        print(f"✅ Analysis complete, returning result")
        return result
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log full error details
        error_details = {
            "error_type": type(e).__name__,
            "error_message": str(e),
            "traceback": traceback.format_exc()
        }
        
        print(f"\n{'='*60}")
        print(f"❌ AUTONOMOUS AGENT ERROR")
        print(f"{'='*60}")
        print(f"Error Type: {error_details['error_type']}")
        print(f"Error Message: {error_details['error_message']}")
        print(f"\nFull Traceback:")
        print(error_details['traceback'])
        print(f"{'='*60}\n")
        
        # Return more detailed error in development
        from config.settings import ENV
        if ENV == "development":
            raise HTTPException(
                status_code=500, 
                detail=f"{error_details['error_type']}: {error_details['error_message']}\n\nTraceback:\n{error_details['traceback']}"
            )
        else:
            raise HTTPException(status_code=500, detail=f"Autonomous agent error: {str(e)}")


@router.post("/autonomous/text")
async def autonomous_analyze_text(
    text: str = Query(..., description="Ingredient text or product information"),
    user_query: str = Query(None, description="Optional user query for context")
):
    """
    AUTONOMOUS AI AGENT - Text Analysis
    
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


@router.get("/autonomous/text/stream")
async def autonomous_analyze_text_stream(
    text: str = Query(..., description="Ingredient text or product information"),
    user_query: str = Query(None, description="Optional user query for context")
):
    """
    AUTONOMOUS AI AGENT - Text Analysis (Streaming)
    
    Returns Server-Sent Events with progressive updates as each step completes.
    Provides real-time feedback instead of waiting for complete analysis.
    
    Events:
    - step_start: New step beginning
    - step_complete: Step finished with results
    - complete: Final comprehensive result
    - error: Error occurred
    """
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    async def event_generator():
        try:
            # Step 1: Initial Analysis
            yield f"data: {json.dumps({'event': 'step_start', 'step': 1, 'name': 'initial_analysis',  'message': 'Analyzing ingredients...'})}\n\n"
            
            initial_result = await ai_service.analyze_text(text)
            
            key_takeaways = []
            if initial_result.trade_offs.pros:
                key_takeaways.extend([f"✓ {pro}" for pro in initial_result.trade_offs.pros[:2]])
            if initial_result.trade_offs.cons:
                key_takeaways.extend([f"⚠ {con}" for con in initial_result.trade_offs.cons[:2]])
            
            initial_analysis = {
                "insight": initial_result.insight,
                "detailed_reasoning": initial_result.detailed_reasoning,
                "trade_offs": initial_result.trade_offs.dict(),
                "key_takeaways": key_takeaways,
                "uncertainty_note": initial_result.uncertainty_note,
                "text": text
            }
            
            yield f"data: {json.dumps({'event': 'step_complete', 'step': 1, 'name': 'initial_analysis', 'result': initial_analysis})}\n\n"
            
            # Step 2: Decision Engine
            yield f"data: {json.dumps({'event': 'step_start', 'step': 2, 'name': 'decision_engine', 'message': 'Running decision engine...'})}\n\n"
            
            request = DecisionRequest(text=text, conversation_context=user_query)
            decision_result = await coordinator.process(request)
            
            decision_data = {
                "quick_insight": decision_result.quick_insight.dict(),
                "explanation": decision_result.explanation.dict(),
                "intent_classified": decision_result.intent_classified,
                "key_signals": decision_result.key_signals,
                "ingredient_translations": [t.dict() for t in decision_result.ingredient_translations],
                "uncertainty_flags": decision_result.uncertainty_flags,
                "structured_analysis": decision_result.structured_analysis.dict() if decision_result.structured_analysis else None
            }
            
            yield f"data: {json.dumps({'event': 'step_complete', 'step': 2, 'name': 'decision_engine', 'result': decision_data})}\n\n"
            
            # Step 3: Synthesis
            yield f"data: {json.dumps({'event': 'step_start', 'step': 3, 'name': 'synthesis', 'message': 'Creating summary...'})}\n\n"
            
            synthesis = {
                "executive_summary": decision_result.quick_insight.summary,
                "key_takeaways": decision_result.explanation.why_this_matters[:3],
                "confidence_level": "low" if len(decision_result.uncertainty_flags) > 2 else "medium" if len(decision_result.uncertainty_flags) > 0 else "high",
                "next_steps": ["Review ingredient translations for details", "Check structured analysis for technical information"]
            }
            
            yield f"data: {json.dumps({'event': 'step_complete', 'step': 3, 'name': 'synthesis', 'result': synthesis})}\n\n"
            
            # Send final complete result
            final_result = {
                "initial_analysis": initial_analysis,
                "workflow_steps": [
                    {"action": "analyze_text", "description": "Initial text analysis", "result": initial_analysis, "reasoning": "Extracted summary and key takeaways"},
                    {"action": "decision_engine", "description": "Deep analysis with multi-agent decision engine", "result": decision_data, "reasoning": "Complete ingredient interpretation and intent classification"}
                ],
                "synthesis": synthesis,
                "total_steps": 2
            }
            
            yield f"data: {json.dumps({'event': 'complete', 'result': final_result})}\n\n"
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            error_data = {"error": str(e), "traceback": traceback.format_exc()}
            yield f"data: {json.dumps({'event': 'error', 'error': error_data})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive"
        }
    )

# ============================================================================
# COMPARISON ENDPOINT (Compare two products side-by-side)
# ============================================================================

@router.post("/compare", response_model=ComparisonResponse)
async def compare_products(request: ComparisonRequest):
    """
    PRODUCT COMPARISON
    
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