"""
Генерация мини-урока по английскому языку (A2-B1) через OpenAI.
Возвращает 4 части: грамматика, практика, письмо, чтение.
"""
import json
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

LESSON_PROMPT = """You are an English teacher for A2-B1 level students.
Generate a mini-lesson in JSON format with exactly 4 parts.

Return ONLY valid JSON, no extra text.

{
  "grammar_questions": [
    {
      "question": "She ___ to school every day.",
      "options": ["go", "goes", "going", "went"],
      "correct": 1,
      "explanation": "We use 'goes' with she/he/it in present simple."
    }
  ],
  "grammar_practice": [
    {
      "sentence": "I usually ___ breakfast at 8 AM.",
      "options": ["have", "has", "had"],
      "correct": 0,
      "explanation": "With 'I' we use 'have', not 'has'."
    }
  ],
  "writing_task": {
    "topic": "Describe your typical morning routine.",
    "hint": "Use present simple. Start with: I wake up at...",
    "example": "I wake up at 7 o'clock. First, I brush my teeth..."
  },
  "reading": {
    "title": "A short passage about daily life",
    "text": "Maria lives in a small town. Every morning she walks to work...",
    "questions": [
      {
        "question": "Where does Maria live?",
        "options": ["In a big city", "In a small town", "In the countryside"],
        "correct": 1
      }
    ]
  }
}

Rules:
- grammar_questions: exactly 5 questions, 4 options each
- grammar_practice: exactly 3 fill-in-the-blank, 3 options each
- writing_task: 1 simple real-life topic
- reading: short passage (5-8 sentences) + 3 comprehension questions
- All content A2-B1 level, clear and simple
- Vary the topics each time (daily life, travel, food, work, hobbies, weather)"""


def handler(event: dict, context) -> dict:
    """Генерирует мини-урок по английскому языку через OpenAI GPT."""
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
    }

    if event.get("httpMethod") == "OPTIONS":
        return {"statusCode": 200, "headers": headers, "body": ""}

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": LESSON_PROMPT}],
        response_format={"type": "json_object"},
        temperature=0.8,
    )

    lesson_data = json.loads(response.choices[0].message.content)

    return {
        "statusCode": 200,
        "headers": headers,
        "body": json.dumps(lesson_data, ensure_ascii=False),
    }
