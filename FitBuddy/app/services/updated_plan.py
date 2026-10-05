from app.config import settings
from app.services.gemini_client import get_gemini_client


def _fallback_updated_plan(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    current_plan: str,
) -> str:
    """
    Local fallback used when Gemini is disabled or unavailable.
    """

    return f"""
FITBUDDY UPDATED WORKOUT PLAN

User: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

UPDATED 7-DAY PLAN

DAY 1 - FULL BODY
• Warm-up: 5-10 minutes
• Squats: 3 x 12
• Push-ups: 3 x 8-12
• Lunges: 3 x 10 each leg
• Plank: 3 x 30 seconds
• Cool-down: 5 minutes

DAY 2 - CARDIO
• Brisk walking: 25-30 minutes
• Light stretching: 10 minutes

DAY 3 - UPPER BODY
• Push-ups: 3 x 10
• Shoulder Press: 3 x 10
• Rows: 3 x 10
• Biceps Curls: 3 x 12
• Triceps Extensions: 3 x 12

DAY 4 - RECOVERY
• Easy walking: 15-20 minutes
• Full-body stretching
• Focus on hydration and sleep

DAY 5 - LOWER BODY
• Squats: 3 x 12
• Lunges: 3 x 10 each leg
• Glute Bridges: 3 x 15
• Calf Raises: 3 x 15
• Plank: 3 x 30 seconds

DAY 6 - FULL BODY
• Jumping Jacks: 3 x 30 seconds
• Squats: 3 x 12
• Push-ups: 3 x 10
• Mountain Climbers: 3 x 20
• Plank: 3 x 30 seconds

DAY 7 - ACTIVE RECOVERY
• Easy walking: 20-30 minutes
• Stretching: 10-15 minutes
• Recovery and rest

PROGRESSION

Increase repetitions or exercise duration gradually
when the current level becomes comfortable.

SAFETY

• Warm up before exercise.
• Maintain proper exercise form.
• Stay hydrated.
• Rest when necessary.
• Stop if you experience pain or unusual symptoms.
• Consult a qualified professional for medical or injury-related concerns.

CURRENT PLAN REFERENCE

{current_plan}
"""


def _build_update_prompt(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    current_plan: str,
) -> str:
    return f"""
You are FitBuddy, an AI workout planning assistant.

Update the user's existing workout plan.

USER INFORMATION

Name: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

CURRENT WORKOUT PLAN

{current_plan}

TASK

Create an improved 7-day workout plan based on the user's information
and the current plan.

REQUIREMENTS

1. Keep the plan realistic.
2. Include warm-up and cool-down guidance.
3. Include exercises with sets and repetitions where appropriate.
4. Include rest or recovery days.
5. Adjust the intensity gradually.
6. Keep the plan easy to understand.
7. Include short safety guidance.
8. Do not diagnose medical conditions.
9. Do not prescribe medication.
10. Do not claim that the plan replaces professional medical advice.

Return only the updated workout plan.
"""


def update_workout_plan(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
    current_plan: str,
) -> str:
    """
    Update an existing workout plan using Gemini.

    If AI is disabled or Gemini is unavailable,
    a local fallback plan is returned.
    """

    if not getattr(settings, "AI_ENABLED", False):
        return _fallback_updated_plan(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            current_plan=current_plan,
        )

    try:
        client = get_gemini_client()

        if client is None:
            return _fallback_updated_plan(
                username=username,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
                current_plan=current_plan,
            )

        prompt = _build_update_prompt(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
            current_plan=current_plan,
        )

        response = client.models.generate_content(
            model=settings.GEMINI_WORKOUT_MODEL,
            contents=prompt,
        )

        text = getattr(response, "text", None)

        if text:
            return text.strip()

    except Exception:
        pass

    return _fallback_updated_plan(
        username=username,
        age=age,
        weight=weight,
        goal=goal,
        intensity=intensity,
        current_plan=current_plan,
    )