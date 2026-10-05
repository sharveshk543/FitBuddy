from app.config import settings
from app.services.gemini_client import get_gemini_client


def _fallback_nutrition_tip(
    username: str,
    age: int,
    weight: float,
    goal: str,
) -> str:
    """
    Local fallback nutrition guidance.

    This is used when Gemini is disabled or unavailable.
    """

    return f"""
FITBUDDY NUTRITION GUIDANCE

User: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}

GENERAL DAILY GUIDANCE

• Include protein-rich foods in your meals.
• Eat a variety of vegetables and fruits.
• Choose whole grains and minimally processed foods when possible.
• Drink water regularly throughout the day.
• Avoid relying heavily on sugary drinks and highly processed snacks.
• Maintain regular meal timing that fits your routine.
• Get adequate sleep and allow your body to recover after exercise.

SIMPLE MEAL IDEAS

Breakfast:
Idli/dosa with sambar, eggs, oats, fruit, or another balanced option.

Lunch:
Rice or chapati with vegetables, dal, curd and a protein source.

Snack:
Fruit, nuts, yogurt/curd, or another simple nutritious snack.

Dinner:
A balanced meal containing vegetables, protein and a suitable carbohydrate source.

IMPORTANT:
Nutrition requirements vary between people. For medical conditions,
food allergies, eating disorders, or specific clinical nutrition needs,
consult a qualified healthcare professional or registered dietitian.
"""


def _build_nutrition_prompt(
    username: str,
    age: int,
    weight: float,
    goal: str,
) -> str:
    return f"""
You are FitBuddy, an AI fitness and nutrition assistant.

Create practical general nutrition guidance for the following user.

Name: {username}
Age: {age}
Weight: {weight} kg
Fitness goal: {goal}

Requirements:

1. Give practical nutrition guidance.
2. Suggest balanced meal ideas.
3. Include protein, vegetables, fruits, carbohydrates and healthy fats.
4. Encourage adequate hydration.
5. Avoid extreme diets.
6. Do not diagnose medical conditions.
7. Do not prescribe medication or supplements.
8. Do not provide unsafe calorie restriction.
9. Clearly state that medical or clinical nutrition needs require a qualified professional.
10. Keep the response easy to read.

Return only the nutrition guidance.
"""


def generate_nutrition_tip_with_flash(
    username: str,
    age: int,
    weight: float,
    goal: str,
) -> str:
    """
    Generate nutrition guidance using Gemini.

    When AI is disabled, the local fallback is returned.
    """

    if not getattr(settings, "AI_ENABLED", False):
        return _fallback_nutrition_tip(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
        )

    try:
        client = get_gemini_client()

        if client is None:
            return _fallback_nutrition_tip(
                username=username,
                age=age,
                weight=weight,
                goal=goal,
            )

        prompt = _build_nutrition_prompt(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
        )

        response = client.models.generate_content(
            model=settings.GEMINI_TIP_MODEL,
            contents=prompt,
        )

        text = getattr(response, "text", None)

        if text:
            return text.strip()

    except Exception:
        pass

    return _fallback_nutrition_tip(
        username=username,
        age=age,
        weight=weight,
        goal=goal,
    )