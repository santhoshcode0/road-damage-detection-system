from collections import Counter


# --------------------------------------------------
# Damage weights
# --------------------------------------------------

DAMAGE_WEIGHTS = {
    "pothole": 4,
    "alligator crack": 4,
    "transverse crack": 2,
    "longitudinal crack": 2,
    "other corruption": 1,
}


def assess_damage(detection_result):
    """
    Analyze YOLO detections and produce a consistent
    preliminary road-condition assessment.

    The assessment is a heuristic and is NOT an
    engineering severity standard.
    """

    detections = detection_result.get(
        "detections",
        []
    )

    total_damages = len(detections)

    # --------------------------------------------------
    # No damage
    # --------------------------------------------------

    if total_damages == 0:

        return {
            "severity_score": 0,
            "road_condition": "Good",
            "risk_level": "Low",
            "maintenance_priority": "Low",
            "repair_category": "No Repair",
            "damage_counts": {},
            "average_confidence": 0.0,
            "assessment_basis": "No visible damage detected."
        }

    # --------------------------------------------------
    # Normalize damage names
    # --------------------------------------------------

    damage_names = [
        d["damage_type"]
        .replace("_", " ")
        .lower()
        for d in detections
    ]

    damage_counts = Counter(
        damage_names
    )

    # --------------------------------------------------
    # Average confidence
    # --------------------------------------------------

    average_confidence = (
        sum(
            d["confidence"]
            for d in detections
        )
        / total_damages
    )

    # --------------------------------------------------
    # Confidence-weighted severity
    # --------------------------------------------------

    severity_score = 0.0

    for detection in detections:

        damage_type = (
            detection["damage_type"]
            .replace("_", " ")
            .lower()
        )

        confidence = detection["confidence"]

        weight = DAMAGE_WEIGHTS.get(
            damage_type,
            1
        )

        severity_score += (
            weight * confidence
        )

    severity_score = round(
        severity_score,
        2
    )

    # --------------------------------------------------
    # Road condition
    # --------------------------------------------------

    if severity_score <= 1.5:

        road_condition = "Good"

    elif severity_score <= 3.5:

        road_condition = "Moderate"

    else:

        road_condition = "Critical"

    # --------------------------------------------------
    # Risk level
    # --------------------------------------------------

    if severity_score <= 1.5:

        risk_level = "Low"

    elif severity_score <= 3.5:

        risk_level = "Medium"

    else:

        risk_level = "High"

    # --------------------------------------------------
    # Maintenance priority
    # --------------------------------------------------

    if severity_score <= 1.5:

        maintenance_priority = "Low"

    elif severity_score <= 2.5:

        maintenance_priority = "Medium"

    elif severity_score <= 4.5:

        maintenance_priority = "High"

    else:

        maintenance_priority = "Immediate"

    # --------------------------------------------------
    # Repair category
    # --------------------------------------------------

    if severity_score <= 1.5:

        repair_category = "Routine"

    elif severity_score <= 3.5:

        repair_category = "Minor"

    elif severity_score <= 5.0:

        repair_category = "Major"

    else:

        repair_category = "Urgent"

    # --------------------------------------------------
    # Human-readable basis
    # --------------------------------------------------

    damage_summary = ", ".join(
        f"{count} {damage}"
        for damage, count
        in damage_counts.items()
    )

    assessment_basis = (
        f"{damage_summary} detected."
    )

    # --------------------------------------------------
    # Return assessment
    # --------------------------------------------------

    return {
        "severity_score": severity_score,
        "road_condition": road_condition,
        "risk_level": risk_level,
        "maintenance_priority": maintenance_priority,
        "repair_category": repair_category,
        "damage_counts": dict(damage_counts),
        "average_confidence": round(
            average_confidence,
            4
        ),
        "assessment_basis": assessment_basis
    }