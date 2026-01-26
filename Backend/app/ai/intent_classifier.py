"""
User Intent Classifier Agent
Very lightweight classification before processing
"""
import google.generativeai as genai
import json
from typing import Literal
from app.ai.key_manager import key_manager

class IntentClassifier:
    def __init__(self):
        if not key_manager:
            self.use_key_manager = False
            return
        self.use_key_manager = True

    async def classify(self, user_input: str) -> Literal["quick_yes_no", "comparison", "risk_check", "curiosity"]:
        """
        Classify user intent from their input.
        Returns one of: quick_yes_no, comparison, risk_check, curiosity
        """
        if not self.use_key_manager:
            # Default to curiosity if AI not available
            return "curiosity"

        prompt = f"""
Classify the user's intent from this input:

"{user_input}"

Return ONLY a JSON object with this exact structure:
{{
    "intent": "quick_yes_no | comparison | risk_check | curiosity"
}}

Intent definitions:
- quick_yes_no: Simple yes/no questions like "Is this healthy?", "Should I eat this?"
- comparison: Comparing products or asking "better than X?"
- risk_check: Asking about risks, allergies, concerns, "Is this safe?"
- curiosity: General questions, "What's in this?", "Tell me about this"

Return JSON only, no other text.
"""

        try:
            # Use key manager with automatic fallback
            async def classify_with_model(model):
                import asyncio
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda: model.generate_content(
                        prompt,
                        generation_config=genai.types.GenerationConfig(
                            response_mime_type="application/json",
                            temperature=0.1  # Low temperature for deterministic classification
                        )
                    )
                )
                return response
            
            response = await key_manager.execute_with_fallback(classify_with_model)
            
            data = json.loads(response.text.strip())
            intent = data.get("intent", "curiosity")
            
            # Validate intent
            valid_intents = ["quick_yes_no", "comparison", "risk_check", "curiosity"]
            if intent not in valid_intents:
                return "curiosity"
            
            return intent
        except Exception as e:
            print(f"Intent classification error: {e}")
            return "curiosity"  # Default fallback

intent_classifier = IntentClassifier()

