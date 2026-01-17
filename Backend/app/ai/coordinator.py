"""
Multi-Agent Coordinator
Orchestrates the decision engine workflow with caching
"""
from app.ai.intent_classifier import intent_classifier
from app.ai.ingredient_interpreter import ingredient_interpreter
from app.ai.decision_engine import decision_engine
from app.ai.explanation_agent import explanation_agent
from app.ai.ingredient_translator import ingredient_translator
from app.ai.service import ai_service
from app.ai.schemas import DecisionRequest, DecisionEngineResponse, QuickInsight
from app.ai.cache import decision_cache

class DecisionEngineCoordinator:
    """
    Coordinates the multi-agent decision engine system.
    Flow: Intent Classification -> Ingredient Interpretation -> Decision -> Explanation + Translation
    """
    
    async def process(self, request: DecisionRequest, conversation_context: str = None) -> DecisionEngineResponse:
        """
        Main orchestration method with parallel processing optimization and caching.
        """
        # Check cache first (skip if conversation context is provided for personalized responses)
        if not conversation_context and not request.conversation_context:
            cached_result = decision_cache.get(request.text)
            if cached_result:
                print(f"⚡ Returning cached decision for: {request.text[:50]}...")
                return DecisionEngineResponse(**cached_result)
        
        # Use conversation context from request if available, otherwise use parameter
        context = request.conversation_context or conversation_context
        
        # Prepare intent text
        intent_text = request.text
        if context:
            intent_text = f"Previous context: {context}\n\nCurrent query: {request.text}"
        
        # PARALLEL PROCESSING OPTIMIZATION:
        # Run intent classification, legacy analysis, and ingredient interpretation concurrently
        import asyncio
        
        async def classify_intent_task():
            """Task wrapper for intent classification"""
            if request.user_intent:
                return request.user_intent
            return await intent_classifier.classify(intent_text)
        
        async def legacy_analysis_task():
            """Task wrapper for legacy insight generation"""
            try:
                return await ai_service.analyze_text(request.text)
            except Exception as e:
                print(f"Legacy insight generation failed: {e}")
                return None
        
        async def interpret_ingredients_task():
            """Task wrapper for ingredient interpretation"""
            return await ingredient_interpreter.interpret(
                ingredient_text=request.text,
                nutrition_info=request.include_nutrition
            )
        
        # Execute all three tasks in parallel
        intent, legacy_analysis, structured_analysis = await asyncio.gather(
            classify_intent_task(),
            legacy_analysis_task(),
            interpret_ingredients_task()
        )
        
        # Step 4: Apply rule-based decision engine (depends on structured_analysis)
        decision = decision_engine.decide(structured_analysis)
        
        # Step 5: Generate consumer-friendly explanation (depends on decision)
        explanation = await explanation_agent.explain(decision)
        
        # Step 6: Use legacy insight as headline, or generate quick insight as fallback
        if legacy_analysis and legacy_analysis.insight:
            quick_insight = QuickInsight(
                summary=legacy_analysis.insight,
                uncertainty_reason=legacy_analysis.uncertainty_note
            )
        else:
            quick_insight = await explanation_agent.generate_quick_insight(decision, structured_analysis)
        
        # Step 7: Translate complex ingredients
        ingredient_translations = await ingredient_translator.translate_ingredients(request.text)
        
        # Create response
        response = DecisionEngineResponse(
            quick_insight=quick_insight,
            explanation=explanation,
            intent_classified=intent,
            key_signals=decision.key_signals,
            ingredient_translations=ingredient_translations,
            uncertainty_flags=structured_analysis.confidence_notes.ambiguity_flags,
            structured_analysis=structured_analysis  # Include for transparency
        )
        
        # Store in cache (skip if conversation context is provided for personalized responses)
        if not conversation_context and not request.conversation_context:
            decision_cache.set(request.text, response.dict())
            print(f"💾 Cached decision for: {request.text[:50]}...")
        
        return response

coordinator = DecisionEngineCoordinator()

