import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def generate_ai_report(detection_result):
    detections = detection_result["detections"]

    if not detections:
        return "No road damage detected in this image."

    damage_summary = "\n".join(
        f"- {d['damage_type']} (confidence: {d['confidence']*100:.1f}%)"
        for d in detections
    )

    prompt = f"""You are a road inspection assistant. Based on the following
detected road damages, write a short, professional inspection report
(3-5 sentences) describing the damage, its likely severity, and a
recommended action for the municipal road maintenance team.

Detected damages:
{damage_summary}

Total damages found: {detection_result['total_damages']}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text