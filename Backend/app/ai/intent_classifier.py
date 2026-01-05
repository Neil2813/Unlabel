"""
User Intent Classifier Agent
Very lightweight classification before processing
"""
import google.generativeai as genai
import json
from typing import Literal
from config.settings import GEMINI_API_KEY

class IntentClassifier:
    def __init__(self):
        if not GEMINI_API_KEY:
            self.model = None
            return
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def classify(self, user_input: str) -> Literal["quick_yes_no", "comparison", "risk_check", "curiosity"]:
        """
        Classify user intent from their input.
        Returns one of: quick_yes_no, comparison, risk_check, curiosity
        """
        if not self.model:
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
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.1  # Low temperature for deterministic classification
                    )
                )
            )
            
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

