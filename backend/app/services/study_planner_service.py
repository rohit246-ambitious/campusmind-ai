import json
from app.utils.gemini_client import ask_gemini


def generate_study_plan(user_input: str):

    prompt = f"""
    You are an expert study planner.

    Based on the user input, generate a day-wise study plan.

    Rules:
    - Return ONLY valid JSON
    - Do NOT add explanation
    - Format must be:
    {{
        "plan": [
            {{"day": 1, "task": "Task description"}},
            {{"day": 2, "task": "Task description"}}
        ]
    }}

    User Input:
    {user_input}
    """

    response = ask_gemini(prompt)

    try:
        return json.loads(response)

    except Exception:
        return {
            "plan": [
                {"day": 1, "task": "AI response failed, try again"}
            ]
        }