"""Worldle game helpers that keep spatial math in the wdo package."""

from __future__ import annotations

import random

from wdo.geometry.bbox import bbox_from_feature
from wdo.geometry.bearing import bearing_to_compass, initial_bearing
from wdo.geometry.distance import haversine_km, haversine_miles

ARROWS = {
    "N": "↑", "NE": "↗", "E": "→", "SE": "↘",
    "S": "↓", "SW": "↙", "W": "←", "NW": "↖",
}


def choose_target(features: list[dict], seed: int | None = None) -> dict:
    """Pick one feature at random, reproducibly when seed is given."""
    if not features:
        raise ValueError("features list is empty")
    return random.Random(seed).choice(features)


def feature_center(feature: dict, method: str = "bbox") -> tuple[float, float]:
    """Return a representative (lat, lon) for Polygon/MultiPolygon feature."""
    method = method.lower()

    if method == "bbox":
        min_lon, min_lat, max_lon, max_lat = bbox_from_feature(feature)
        return ((min_lat + max_lat) / 2.0, (min_lon + max_lon) / 2.0)

    if method == "mean":
        geometry = feature.get("geometry", {})
        geom_type = geometry.get("type")
        coords = geometry.get("coordinates", [])

        points: list[tuple[float, float]] = []
        if geom_type == "Polygon":
            for ring in coords:
                for lon, lat in ring:
                    points.append((lat, lon))
        elif geom_type == "MultiPolygon":
            for poly in coords:
                for ring in poly:
                    for lon, lat in ring:
                        points.append((lat, lon))
        else:
            raise ValueError(f"Unsupported geometry type: {geom_type}")

        if not points:
            raise ValueError("Feature has no coordinates")

        mean_lat = sum(p[0] for p in points) / len(points)
        mean_lon = sum(p[1] for p in points) / len(points)
        return (mean_lat, mean_lon)

    raise ValueError("method must be 'bbox' or 'mean'")


def guess_feedback(guess_feature: dict, target_feature: dict) -> dict:
    """Return correctness, distance, bearing, compass, and arrow for a guess."""
    guess_iso3 = guess_feature.get("properties", {}).get("ISO_A3")
    target_iso3 = target_feature.get("properties", {}).get("ISO_A3")
    correct = guess_iso3 == target_iso3

    guess_center = feature_center(guess_feature, method="bbox")
    target_center = feature_center(target_feature, method="bbox")

    distance_km = haversine_km(guess_center, target_center)
    distance_miles = haversine_miles(guess_center, target_center)
    bearing_deg = initial_bearing(guess_center, target_center)
    compass = bearing_to_compass(bearing_deg)

    return {
        "correct": correct,
        "distance_km": distance_km,
        "distance_miles": distance_miles,
        "bearing_deg": bearing_deg,
        "compass": compass,
        "arrow": ARROWS.get(compass, "?"),
    }


def format_feedback(result: dict, units: str = "km") -> str:
    """Return plain-text feedback string for logs/tests before UI rendering."""
    if result.get("correct"):
        return "Correct! 🎉"

    units = units.lower()
    if units == "miles":
        distance = result.get("distance_miles", 0.0)
        unit_label = "miles"
    else:
        distance = result.get("distance_km", 0.0)
        unit_label = "km"

    arrow = result.get("arrow", "?")
    compass = result.get("compass", "?")
    return f"{arrow} {compass} • {distance:,.1f} {unit_label}"
