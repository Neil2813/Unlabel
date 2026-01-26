"""
Food Ingredient Interpreter Agent
Converts ingredient/nutrition info into structured, neutral signals
"""
import google.generativeai as genai
import json
from config.settings import GEMINI_API_KEY
from app.ai.schemas import StructuredIngredientAnalysis

class IngredientInterpreter:
    def __init__(self):
        if not GEMINI_API_KEY:
            self.model = None
            return
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def interpret(self, ingredient_text: str, nutrition_info: str = None) -> StructuredIngredientAnalysis:
        """
        Analyze ingredients and convert to structured signals.
        Does NOT give verdicts or recommendations.
        """
        if not self.model:
            raise ValueError("AI Service not configured (Missing API Key)")

        system_prompt = """You are a food-ingredient interpretation assistant.

Your role is to ANALYZE food ingredient and nutrition information
and CONVERT it into structured, neutral signals.

You MUST NOT:
- Give medical advice
- Label foods as "healthy" or "unhealthy"
- Make disease-related claims
- Give consumption recommendations

You MUST:
- Focus only on ingredient properties
- Use neutral, consumer-friendly reasoning
- Be consistent and deterministic

Your output will be used by a separate rule-based decision engine."""

        user_prompt = f"""Analyze the following food product information.

TASK:
Convert the input into structured food properties.
Do NOT give a verdict or recommendation.

INPUT:
{ingredient_text}
{f'Nutrition Info: {nutrition_info}' if nutrition_info else ''}

OUTPUT FORMAT (STRICT JSON):

{{
  "ingredient_summary": {{
    "primary_components": [],
    "added_sugars_present": true/false,
    "sweetener_type": "none | natural | added | mixed",
    "fiber_level": "none | low | moderate | high",
    "protein_level": "none | low | moderate | high",
    "fat_level": "none | low | moderate | high",
    "processing_level": "low | moderate | high",
    "ultra_processed_markers": [],
    "ingredient_count": number
  }},
  "food_properties": {{
    "sugar_dominant": true/false,
    "fiber_protein_support": "none | weak | moderate | strong",
    "energy_release_pattern": "rapid | mixed | slow",
    "satiety_support": "low | moderate | high",
    "formulation_complexity": "simple | moderate | complex"
  }},
  "confidence_notes": {{
    "data_completeness": "high | medium | low",
    "ambiguity_flags": []
  }}
}}

IMPORTANT RULES:
- If information is missing, infer conservatively.
- If uncertain, flag it in ambiguity_flags.
- Do NOT explain your reasoning.
- Do NOT add extra fields."""

        try:
            import asyncio
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.model.generate_content(
                    [system_prompt, user_prompt],
                    generation_config=genai.types.GenerationConfig(
                        response_mime_type="application/json",
                        temperature=0.2  # Low temperature for consistency
                    )
                )
            )
            
            data = json.loads(response.text.strip())
            return StructuredIngredientAnalysis(**data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            print(f"Response text: {response.text if 'response' in locals() else 'N/A'}")
            raise ValueError(f"Failed to parse structured analysis: {e}")
        except Exception as e:
            print(f"Ingredient interpretation error: {e}")
            raise

ingredient_interpreter = IngredientInterpreter()

