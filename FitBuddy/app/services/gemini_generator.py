from typing import Any

from app.config import settings
from app.services.gemini_client import get_gemini_client


def _demo_workout_plan(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    """
    Fallback workout plan used when AI is disabled
    or Gemini is unavailable.
    """

    return f"""
FITBUDDY PERSONALIZED 7-DAY WORKOUT PLAN

User: {username}
Age: {age}
Weight: {weight} kg
Goal: {goal}
Intensity: {intensity}

DAY 1 - FULL BODY
• Warm-up: 5-10 minutes
• Bodyweight Squats: 3 x 12
• Push-ups: 3 x 8-12
• Lunges: 3 x 10 each leg
• Plank: 3 x 30 seconds
• Cool-down: 5 minutes

DAY 2 - CARDIO
• Brisk walking: 20-30 minutes
• Light jogging: 10 minutes
• Stretching: 10 minutes

DAY 3 - UPPER BODY
• Push-ups: 3 x 10
• Shoulder Press: 3 x 10
• Bent-over Row: 3 x 10
• Biceps Curl: 3 x 12
• Triceps Extension: 3 x 12

DAY 4 - REST & RECOVERY
• Light walking: 15-20 minutes
• Full-body stretching
• Focus on hydration and sleep

DAY 5 - LOWER BODY
• Squats: 3 x 12
• Lunges: 3 x 10 each leg
• Glute Bridge: 3 x 15
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
• Relax and recover

GENERAL TIPS
• Warm up before exercising.
• Drink enough water.
• Maintain good exercise form.
• Increase intensity gradually.
• Take rest if you experience pain or unusual discomfort.
• Consult a qualified professional for medical or injury-related concerns.
"""


def _build_prompt(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    return f"""
You are FitBuddy, an AI fitness planning assistant.

Create a safe, practical and personalized 7-day workout plan.

USER INFORMATION
Name: {username}
Age: {age}
Weight: {weight} kg
Fitness Goal: {goal}
Workout Intensity: {intensity}

REQUIREMENTS
1. Create a 7-day plan.
2. Include warm-up and cool-down guidance.
3. Include exercises, sets and repetitions where appropriate.
4. Include rest or recovery days.
5. Keep the plan realistic for the requested intensity.
6. Give short safety guidance.
7. Format the answer clearly using headings for each day.
8. Do not diagnose medical conditions.
9. Do not claim that the plan replaces professional medical advice.

Return only the workout plan.
"""


def generate_workout_gemini(
    username: str,
    age: int,
    weight: float,
    goal: str,
    intensity: str,
) -> str:
    """
    Generate a personalized workout plan.

    If AI_ENABLED=false, the application uses the local
    fallback plan so the project can be tested without
    a Gemini API key.
    """

    if not getattr(settings, "AI_ENABLED", False):
        return _demo_workout_plan(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

    try:
        client = get_gemini_client()

        if client is None:
            return _demo_workout_plan(
                username=username,
                age=age,
                weight=weight,
                goal=goal,
                intensity=intensity,
            )

        prompt = _build_prompt(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

        response = client.models.generate_content(
            model=settings.GEMINI_WORKOUT_MODEL,
            contents=prompt,
        )

        text = getattr(response, "text", None)

        if text:
            return text.strip()

        return _demo_workout_plan(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )

    except Exception:
        # Keep the application usable even if Gemini
        # is unavailable, the key is invalid, or the
        # network request fails.
        return _demo_workout_plan(
            username=username,
            age=age,
            weight=weight,
            goal=goal,
            intensity=intensity,
        )