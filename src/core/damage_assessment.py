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


# --------------------------------------------------
# Additional severity multipliers
# --------------------------------------------------

DAMAGE_MULTIPLIERS = {
    "pothole": 1.15,
    "alligator crack": 1.15,
    "transverse crack": 1.00,
    "longitudinal crack": 1.00,
    "other corruption": 0.80,
}


def normalize_damage_name(damage_type):
    """
    Convert damage names into a consistent format.
    """

    return (
        damage_type
        .replace("_", " ")
        .strip()
        .lower()
    )


def assess_damage(detection_result):
    """
    Analyze YOLO detections and produce a consistent
    preliminary road-condition assessment.

    This is a heuristic assessment based only on
    visible detections. It is NOT an engineering
    severity standard.
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

            "assessment_basis":
                "No visible damage detected."

        }

    # --------------------------------------------------
    # Normalize damage names
    # --------------------------------------------------

    damage_names = [
        normalize_damage_name(
            d["damage_type"]
        )
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
    # Base severity
    # --------------------------------------------------

    severity_score = 0.0

    for detection in detections:

        damage_type = normalize_damage_name(
            detection["damage_type"]
        )

        confidence = float(
            detection["confidence"]
        )

        weight = DAMAGE_WEIGHTS.get(
            damage_type,
            1
        )

        multiplier = DAMAGE_MULTIPLIERS.get(
            damage_type,
            1.0
        )

        contribution = (
            weight
            * confidence
            * multiplier
        )

        severity_score += contribution

    # --------------------------------------------------
    # Repeated-damage factor
    #
    # Multiple visible defects should increase
    # maintenance concern, but not linearly forever.
    # --------------------------------------------------

    if total_damages >= 2:

        additional_damage_factor = min(
            1.0 + (
                0.10
                * (total_damages - 1)
            ),
            1.50
        )

        severity_score *= (
            additional_damage_factor
        )

    # --------------------------------------------------
    # Multiple severe damage types
    # --------------------------------------------------

    severe_damage_types = {
        "pothole",
        "alligator crack"
    }

    severe_damage_count = sum(
        count
        for damage_type, count
        in damage_counts.items()
        if damage_type in severe_damage_types
    )

    if severe_damage_count >= 2:

        severity_score *= 1.10

    # --------------------------------------------------
    # Round final score
    # --------------------------------------------------

    severity_score = round(
        severity_score,
        2
    )

    # --------------------------------------------------
    # Road condition
    # --------------------------------------------------

    if severity_score <= 1.5:

        road_condition = "Good"

    elif severity_score < 4.0:

        road_condition = "Moderate"

    else:

        road_condition = "Critical"

    # --------------------------------------------------
    # Risk level
    # --------------------------------------------------

    if severity_score <= 1.5:

        risk_level = "Low"

    elif severity_score < 4.0:

        risk_level = "Medium"

    else:

        risk_level = "High"

    # --------------------------------------------------
    # Maintenance priority
    #
    # Immediate starts at 4.0 as requested.
    # --------------------------------------------------

    if severity_score <= 1.5:

        maintenance_priority = "Low"

    elif severity_score < 2.5:

        maintenance_priority = "Medium"

    elif severity_score < 4.0:

        maintenance_priority = "High"

    else:

        maintenance_priority = "Immediate"

    # --------------------------------------------------
    # Repair category
    # --------------------------------------------------

    if severity_score <= 1.5:

        repair_category = "Routine"

    elif severity_score < 4.0:

        repair_category = "Minor"

    elif severity_score <= 6.0:

        repair_category = "Major"

    else:

        repair_category = "Urgent"

    # --------------------------------------------------
    # Human-readable assessment basis
    # --------------------------------------------------

    damage_summary = ", ".join(
        f"{count} {damage}"
        for damage, count
        in damage_counts.items()
    )

    assessment_basis = (
        f"{damage_summary} detected. "
        f"Severity score: {severity_score}."
    )

    # --------------------------------------------------
    # Return assessment
    # --------------------------------------------------

    return {

        "severity_score":
            severity_score,

        "road_condition":
            road_condition,

        "risk_level":
            risk_level,

        "maintenance_priority":
            maintenance_priority,

        "repair_category":
            repair_category,

        "damage_counts":
            dict(damage_counts),

        "average_confidence":
            round(
                average_confidence,
                4
            ),

        "assessment_basis":
            assessment_basis

    }