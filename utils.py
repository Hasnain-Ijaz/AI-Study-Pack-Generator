import json
import os
import re
import time

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MAX_RETRIES = 3
MODEL = "openai/gpt-oss-120b"


def get_api_key():
    return os.getenv("GROQ_API_KEY", "").strip()


def validate_inputs(subject, topic):
    if not subject or not subject.strip():
        raise ValueError("Subject is required.")
    if not topic or not topic.strip():
        raise ValueError("Topic is required.")


def extract_json(text):
    text = text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\s*```$", "", text)

    try:
        data = json.loads(text)
        if isinstance(data, dict):
            return data
    except json.JSONDecodeError:
        pass

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("AI response did not contain valid JSON.")

    data = json.loads(match.group(0))

    if not isinstance(data, dict):
        raise ValueError("AI response JSON must be an object.")

    return data


def call_ai(client, system_prompt, user_prompt, stage_name):
    last_error = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.3,
                max_tokens=7000,
            )

            text = response.choices[0].message.content or ""
            return extract_json(text)

        except Exception as exc:
            last_error = exc
            if attempt < MAX_RETRIES:
                time.sleep(2 * attempt)

    raise RuntimeError(
        f"{stage_name} stage failed after {MAX_RETRIES} attempts: {last_error}"
    )
