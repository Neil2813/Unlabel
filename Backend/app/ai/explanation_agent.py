"""
Consumer Explanation Agent
Explains pre-computed decisions clearly and calmly
"""
import google.generativeai as genai
import json
from config.settings import GEMINI_API_KEY
from app.ai.schemas import Decision, ConsumerExplanation, QuickInsight, StructuredIngredientAnalysis

class ExplanationAgent:
    def __init__(self):
        if not GEMINI_API_KEY:
            self.model = None
            return
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def generate_quick_insight(
        self, 
        decision: Decision, 
        structured_analysis: StructuredIngredientAnalysis
    ) -> QuickInsight:
        """
        Generate a one-line summary for instant understanding.
        """
        if not self.model:
            return QuickInsight(
                summary="Product analyzed based on its ingredient profile.",
                uncertainty_reason=None
            )

        system_prompt = """You are a food intelligence assistant.

Generate a ONE-SENTENCE summary that gives instant understanding.
Be clear, direct, and avoid jargon. Focus on what matters most to the consumer.
DO NOT use phrases like "frequent use", "infrequently", "should be consumed", or similar consumption frequency language.
Focus on what the product IS, not how often to eat it."""

        user_prompt = f"""Create a one-sentence summary for this product:

Key Signals: {', '.join(decision.key_signals[:3])}
Processing Level: {structured_analysis.ingredient_summary.processing_level}
Sugar Dominant: {structured_analysis.food_properties.sugar_dominant}
Energy Release: {structured_analysis.food_properties.energy_release_pattern}

Return JSON:
{{
  "summary": "One clear sentence (max 15 words) that captures the essence. Example: 'Fortified whole grain cereal with added sugars - good for quick energy but may cause energy dips.'",
  "uncertainty_reason": "null or brief reason if information is incomplete"
}}

Keep it simple and actionable."""

        try:
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    [system_prompt, user_prompt],
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.4
                    )
                )
            )
            
            data = json.loads(response.text.strip())
            return QuickInsight(**data)
        except Exception as e:
            print(f"Quick insight generation error: {e}")
            # Create a simple fallback based on key signals
            if decision.key_signals:
                signal_summary = decision.key_signals[0].lower()
                return QuickInsight(
                    summary=f"{signal_summary} - analyzed based on ingredient profile."
                )
            return QuickInsight(
                summary="Analyzed based on ingredient profile."
            )

    async def explain(self, decision: Decision) -> ConsumerExplanation:
        """
        Generate consumer-friendly explanation of the decision.
        """
        if not self.model:
            # Fallback explanation
            return ConsumerExplanation(
                why_this_matters=["Processing level affects nutrient availability", "Ingredient composition impacts energy release"],
                when_it_makes_sense="Consider your individual needs and context",
                what_to_know="This is informational, not medical advice"
            )

        system_prompt = """You are a consumer food explanation assistant.

Your job is to explain a pre-computed decision clearly and calmly.

You MUST:
- Use simple, everyday language
- Avoid fear-based tone
- Avoid medical claims
- Be concise and actionable
- Focus on practical implications, not technical details
- DO NOT use phrases like "frequent use", "infrequently", "should be consumed", or similar consumption frequency language
- Focus on what the product IS and its characteristics, not consumption frequency"""

        user_prompt = f"""Using the key signals below, explain the product characteristics to a general consumer.

KEY SIGNALS:
{chr(10).join(f'- {signal}' for signal in decision.key_signals)}

OUTPUT FORMAT (STRICT JSON):

{{
  "why_this_matters": [
    "One short sentence about the most important factor (max 12 words)",
    "One short sentence about the second factor (max 12 words)",
    "One short sentence about the third factor (max 12 words)"
  ],
  "when_it_makes_sense": "One clear sentence (max 15 words) about when this product fits well",
  "what_to_know": "One brief sentence (max 15 words) with key takeaway"
}}

EXAMPLES:
- "why_this_matters": ["Contains whole grains for fiber", "Fortified with vitamins and minerals", "Added sugars may cause energy spikes"]
- "when_it_makes_sense": "Good for breakfast when you need quick energy and nutrients."
- "what_to_know": "Pair with protein to balance energy release throughout the morning."

Keep it simple, practical, and avoid technical jargon."""

        try:
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    [system_prompt, user_prompt],
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.5  # Slightly higher for natural language
                    )
                )
            )
            
            data = json.loads(response.text.strip())
            
            # Remove verdict if present
            if "verdict" in data:
                del data["verdict"]
            
            # Limit why_this_matters to 3 items
            if "why_this_matters" in data and isinstance(data["why_this_matters"], list):
                data["why_this_matters"] = data["why_this_matters"][:3]
            
            return ConsumerExplanation(**data)
        except Exception as e:
            print(f"Explanation generation error: {e}")
            # Fallback
            return ConsumerExplanation(
                why_this_matters=decision.key_signals[:3] if len(decision.key_signals) >= 3 else decision.key_signals,
                when_it_makes_sense="Consider your individual dietary needs and preferences",
                what_to_know="This analysis is informational and not medical advice"
            )

explanation_agent = ExplanationAgent()

