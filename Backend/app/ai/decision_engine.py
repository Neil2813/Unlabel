"""
Rule-based Decision Engine
Takes structured signals and makes decisions
"""
from app.ai.schemas import StructuredIngredientAnalysis, Decision

class DecisionEngine:
    """
    Transparent, rule-based decision engine.
    Processes structured ingredient analysis and produces verdicts.
    """
    
    def decide(self, analysis: StructuredIngredientAnalysis) -> Decision:
        """
        Apply rules to structured analysis and produce a decision.
        """
        signals = []
        score = 0  # Higher = better for daily use
        
        # Rule 1: Processing Level
        if analysis.ingredient_summary.processing_level == "low":
            score += 3
            signals.append("Minimally processed")
        elif analysis.ingredient_summary.processing_level == "moderate":
            score += 1
            signals.append("Moderately processed")
        else:  # high
            score -= 2
            signals.append("Highly processed")
        
        # Rule 2: Ultra-processed markers
        if len(analysis.ingredient_summary.ultra_processed_markers) > 0:
            score -= len(analysis.ingredient_summary.ultra_processed_markers) * 0.5
            signals.append(f"Contains {len(analysis.ingredient_summary.ultra_processed_markers)} ultra-processed marker(s)")
        
        # Rule 3: Sugar dominance
        if analysis.food_properties.sugar_dominant:
            score -= 2
            signals.append("Sugar-dominant formulation")
        else:
            score += 1
        
        # Rule 4: Added sugars
        if analysis.ingredient_summary.added_sugars_present:
            score -= 1.5
            signals.append("Contains added sugars")
        
        # Rule 5: Fiber/Protein support
        if analysis.food_properties.fiber_protein_support == "strong":
            score += 2
            signals.append("Strong fiber/protein support")
        elif analysis.food_properties.fiber_protein_support == "moderate":
            score += 1
            signals.append("Moderate fiber/protein support")
        elif analysis.food_properties.fiber_protein_support == "weak":
            score -= 0.5
            signals.append("Weak fiber/protein support")
        else:  # none
            score -= 1
            signals.append("No fiber/protein support")
        
        # Rule 6: Energy release pattern
        if analysis.food_properties.energy_release_pattern == "slow":
            score += 1.5
            signals.append("Slow energy release")
        elif analysis.food_properties.energy_release_pattern == "mixed":
            score += 0.5
        else:  # rapid
            score -= 1
            signals.append("Rapid energy release")
        
        # Rule 7: Satiety support
        if analysis.food_properties.satiety_support == "high":
            score += 1.5
            signals.append("High satiety support")
        elif analysis.food_properties.satiety_support == "moderate":
            score += 0.5
        else:  # low
            score -= 0.5
            signals.append("Low satiety support")
        
        # Rule 8: Ingredient count (simpler = generally better)
        if analysis.ingredient_summary.ingredient_count <= 5:
            score += 0.5
        elif analysis.ingredient_summary.ingredient_count > 15:
            score -= 0.5
            signals.append("High ingredient count")
        
        # Keep top 3 most impactful signals
        key_signals = signals[:3] if len(signals) <= 3 else signals[:3]
        
        return Decision(
            key_signals=key_signals
        )

decision_engine = DecisionEngine()

