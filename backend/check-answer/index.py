"""
Проверка письменного задания пользователя через OpenAI.
Принимает текст пользователя и тему, возвращает оценку и советы.
"""
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def handler(event: dict, context) -> dict:
    """Проверяет письменный ответ студента и даёт обратную связь."""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    body = json.loads(event.get("body", "{}"))
    user_text = body.get("text", "")
    topic = body.get("topic", "")

    if not user_text:
        return {
            "statusCode": 400,
            "headers": headers,
            "body": json.dumps({"error": "No text provided"}),
        }

    prompt = f"""You are a friendly English teacher for A2-B1 level.
The student was asked to write 5-7 sentences about: "{topic}"

Student's text:
"{user_text}"

Evaluate and return ONLY valid JSON:
{{
  "score": 85,
  "level": "Good",
  "feedback": "Your sentences are clear and well structured!",
  "corrections": [
    {{"original": "I goes to shop", "corrected": "I go to the shop", "explanation": "With 'I' use base form 'go'"}}
  ],
  "positive": "Great use of present simple tense!",
  "tip": "Try to use more connecting words like 'then', 'after that', 'finally'."
}}

Rules:
- score: 0-100
- level: "Needs work" / "Good" / "Excellent"
- corrections: list only real mistakes (max 3), empty array if no mistakes
- feedback: 1-2 encouraging sentences
- Keep tone friendly and motivating
- If text is empty or gibberish, score = 0"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"},
        temperature=0.3,
    )

    result = json.loads(response.choices[0].message.content)

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(result, ensure_ascii=False),
    }
