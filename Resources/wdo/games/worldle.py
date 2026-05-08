import random

from wdo.geometry.bbox import bbox_from_feature
from wdo.geometry.distance import haversine_km, haversine_miles
from wdo.geometry.bearing import initial_bearing, bearing_to_compass


ARROWS = {
    "N": "↑",
    "NE": "↗",
    "E": "→",
    "SE": "↘",
    "S": "↓",
    "SW": "↙",
    "W": "←",
    "NW": "↖",
}


def _coords_from_geometry(geometry):
    """
    Flatten Polygon or MultiPolygon coordinates into a list of (lon, lat) pairs.
    """
    geom_type = geometry["type"]
    coords = geometry["coordinates"]

    points = []

    if geom_type == "Polygon":
        for ring in coords:
            for lon, lat in ring:
                points.append((lon, lat))

    elif geom_type == "MultiPolygon":
        for polygon in coords:
            for ring in polygon:
                for lon, lat in ring:
                    points.append((lon, lat))

    else:
        raise ValueError(f"Unsupported geometry type: {geom_type}")

    return points


def choose_target(features, seed=None):
    """
    Pick one country feature at random.
    If seed is given, the result is reproducible.
    """
    rng = random.Random(seed)
    return rng.choice(features)


def feature_center(feature, method="bbox"):
    """
    Return a representative (lat, lon) point for a country feature.

    method="bbox" gives the center of the bounding box.
    method="mean" gives the average of all boundary vertices.
    """
    if method == "bbox":
        min_lon, min_lat, max_lon, max_lat = bbox_from_feature(feature)
        lat = (min_lat + max_lat) / 2
        lon = (min_lon + max_lon) / 2
        return lat, lon

    if method == "mean":
        points = _coords_from_geometry(feature["geometry"])
        lons = [p[0] for p in points]
        lats = [p[1] for p in points]
        return sum(lats) / len(lats), sum(lons) / len(lons)

    raise ValueError("method must be 'bbox' or 'mean'")


def guess_feedback(guess_feature, target_feature):
    """
    Compare a guess to the target and return distance, bearing, compass, and arrow.
    Bearing points from the guessed country toward the target country.
    """
    guess_name = guess_feature["properties"].get("ADMIN")
    target_name = target_feature["properties"].get("ADMIN")

    guess_iso3 = guess_feature["properties"].get("ISO_A3")
    target_iso3 = target_feature["properties"].get("ISO_A3")

    correct = guess_iso3 == target_iso3

    guess_center = feature_center(guess_feature)
    target_center = feature_center(target_feature)

    distance_km = haversine_km(guess_center, target_center)
    distance_miles = haversine_miles(guess_center, target_center)

    bearing_deg = initial_bearing(guess_center, target_center)
    compass = bearing_to_compass(bearing_deg)
    arrow = ARROWS.get(compass, "?")

    return {
        "correct": correct,
        "guess_name": guess_name,
        "target_name": target_name,
        "guess_iso3": guess_iso3,
        "target_iso3": target_iso3,
        "distance_km": distance_km,
        "distance_miles": distance_miles,
        "bearing_deg": bearing_deg,
        "compass": compass,
        "arrow": arrow,
    }


def format_feedback(result, units="km"):
    """
    Return a plain-text feedback message for one guess.
    """
    if result["correct"]:
        return f"Correct! The country was {result['target_name']}."

    if units == "miles":
        distance = result["distance_miles"]
        label = "miles"
    else:
        distance = result["distance_km"]
        label = "km"

    return (
        f"{result['guess_name']} {result['arrow']} "
        f"{distance:,.0f} {label} away"
    )