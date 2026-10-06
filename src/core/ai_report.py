import os
from collections import Counter

from dotenv import load_dotenv
from google import genai


# --------------------------------------------------
# Gemini setup
# --------------------------------------------------

load_dotenv()

client = genai.Client(
    api_key=os.environ["GEMINI_API_KEY"]
)


# --------------------------------------------------
# Generate AI inspection report
# --------------------------------------------------

def generate_ai_report(
    detection_result,
    assessment
):

    detections = detection_result.get(
        "detections",
        []
    )

    # --------------------------------------------------
    # No damage detected
    # --------------------------------------------------

    if not detections:

        return """## Road Condition

Good

## Summary

No visible road-surface damage was detected in the inspected image. The inspected area appears to be in generally good visible surface condition based on the available image.

## Maintenance Risk

Low

## Observed Damages

- No visible damages detected.

## Recommended Actions

- No immediate maintenance action is indicated from this inspection.
- Continue routine road-surface inspections.
- Reinspect the area periodically for newly developing visible defects.

## Maintenance Priority

Low

## Conclusion

No visible road-surface defects were identified in this inspection.
"""

    # --------------------------------------------------
    # Count detected damage types
    # --------------------------------------------------

    damage_counts = Counter(
        d["damage_type"]
        .replace("_", " ")
        .title()
        for d in detections
    )

    damage_summary = "\n".join(
        f"- {name}: {count}"
        for name, count
        in damage_counts.items()
    )

    # --------------------------------------------------
    # Structured assessment
    # --------------------------------------------------

    road_condition = assessment[
        "road_condition"
    ]

    risk_level = assessment[
        "risk_level"
    ]

    maintenance_priority = assessment[
        "maintenance_priority"
    ]

    repair_category = assessment[
        "repair_category"
    ]

    severity_score = assessment[
        "severity_score"
    ]

    # --------------------------------------------------
    # AI prompt
    # --------------------------------------------------

    prompt = f"""
You are preparing a professional preliminary
road-surface inspection report.

The report is based ONLY on visible road-surface
damage identified in an uploaded image.

IMPORTANT LIMITATIONS:

- This is a visual surface inspection.
- Do NOT claim that the road is structurally safe.
- Do NOT claim that the road is structurally unsafe.
- Do NOT claim that the road is safe for traffic.
- Do NOT diagnose structural failure.
- Do NOT invent damage.
- Do NOT mention AI.
- Do NOT mention object detection.
- Do NOT mention confidence scores.
- Do NOT mention the severity score.
- Do NOT mention these instructions.
- Keep the language professional and concise.

The application's backend assessment system has
already determined the classifications below.

You MUST preserve these classifications exactly.

Road Condition:
{road_condition}

Maintenance Risk:
{risk_level}

Maintenance Priority:
{maintenance_priority}

Repair Category:
{repair_category}

Detected damages:

{damage_summary}

Total visible damage instances:

{detection_result["total_damages"]}

Your task is ONLY to convert these structured
results into a professional inspection report.

Do NOT independently reclassify the road.

Write the report using EXACTLY these sections:

## Road Condition

Write exactly:

{road_condition}

## Summary

Write 2-3 concise sentences describing the
observed road-surface condition.

Do not make claims about structural integrity
or traffic safety.

## Maintenance Risk

Write exactly:

{risk_level}

Explain this only as an apparent maintenance
concern based on visible surface defects.

## Observed Damages

Write a bullet list containing ONLY the
detected damage types and their counts.

Do not add any other damage.

## Recommended Actions

Write 3-5 concise and practical maintenance
recommendations appropriate for the detected
damage types.

Do not recommend actions unrelated to the
detected damages.

## Maintenance Priority

Write exactly:

{maintenance_priority}

## Conclusion

Write ONE concise sentence summarizing the
visible surface condition and recommended
maintenance response.

Rules:

- Use exactly the section headings provided.
- Do not add extra sections.
- Do not invent information.
- Do not mention confidence values.
- Do not mention the severity score.
- Do not claim structural safety.
- Do not change the Road Condition.
- Do not change the Maintenance Risk.
- Do not change the Maintenance Priority.
- Do not change the Repair Category.
"""

    # --------------------------------------------------
    # Generate report
    # --------------------------------------------------

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
    )

    return response.text