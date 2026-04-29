"""Core gameplay helpers for the Worldle assignment."""

from __future__ import annotations

import random

from ..geometry.bbox import bbox_from_feature
from ..geometry.distance import haversine_distance_km, initial_bearing, bearing_to_compass

ARROWS = {
    "N": "↑", "NE": "↗", "E": "→", "SE": "↘",
    "S": "↓", "SW": "↙", "W": "←", "NW": "↖",
}


def choose_target(features: list[dict], seed: int | None = None) -> dict:
    """Choose one target feature from the list. Optional seed makes it reproducible."""
    if not features:
        raise ValueError("features list is empty")
    rng = random.Random(seed)
    return rng.choice(features)


def feature_center(feature: dict) -> tuple[float, float]:
    """Return center as (lat, lon) using the feature bounding box midpoint."""
    min_lon, min_lat, max_lon, max_lat = bbox_from_feature(feature)
    return ((min_lat + max_lat) / 2.0, (min_lon + max_lon) / 2.0)


def guess_feedback(guess_feature: dict, target_feature: dict) -> dict:
    """Return guess result details including direction and distance to target."""
    guess_center = feature_center(guess_feature)
    target_center = feature_center(target_feature)

    lat1, lon1 = guess_center
    lat2, lon2 = target_center

    distance_km = haversine_distance_km(lat1, lon1, lat2, lon2)
    bearing = initial_bearing(lat1, lon1, lat2, lon2)
    compass = bearing_to_compass(bearing)

    guess_name = guess_feature.get("properties", {}).get("ADMIN", "Unknown")
    target_name = target_feature.get("properties", {}).get("ADMIN", "Unknown")
    correct = guess_name == target_name

    return {
        "correct": correct,
        "guess_name": guess_name,
        "target_name": target_name,
        "distance_km": distance_km,
        "bearing": bearing,
        "compass": compass,
        "arrow": ARROWS.get(compass, "?"),
    }


def format_feedback(feedback: dict) -> str:
    """Format a feedback dictionary into plain text for display/logging."""
    if feedback.get("correct"):
        return f"✅ Correct! The country is {feedback.get('target_name', 'Unknown')}."
    return (
        f"{feedback.get('arrow', '?')} {feedback.get('compass', '?')} • "
        f"{feedback.get('distance_km', 0.0):,.1f} km from target"
    )
