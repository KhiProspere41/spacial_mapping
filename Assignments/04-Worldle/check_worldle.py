"""Small sanity checks for Assignment 04 Worldle helpers."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
RESOURCES = ROOT / "Resources"
if str(RESOURCES) not in sys.path:
    sys.path.insert(0, str(RESOURCES))

from wdo.geometry.bbox import bbox_from_feature
from wdo.geometry.distance import haversine_distance_km, initial_bearing, bearing_to_compass
from wdo.games.worldle import choose_target, feature_center, guess_feedback, format_feedback


def run_checks():
    feature = {
        "type": "Feature",
        "properties": {"ADMIN": "Demo", "ISO_A3": "DMO"},
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[-100.0, 30.0], [-99.0, 30.0], [-99.0, 31.0], [-100.0, 31.0], [-100.0, 30.0]]],
        },
    }

    assert bbox_from_feature(feature) == (-100.0, 30.0, -99.0, 31.0)
    assert choose_target([feature], seed=1)["properties"]["ADMIN"] == "Demo"

    lat, lon = feature_center(feature)
    assert round(lat, 1) == 30.5 and round(lon, 1) == -99.5

    d = haversine_distance_km(30.5, -99.5, 30.5, -99.5)
    assert round(d, 6) == 0.0

    b = initial_bearing(30.0, -100.0, 31.0, -99.0)
    c = bearing_to_compass(b)
    assert c in {"N", "NE", "E", "SE", "S", "SW", "W", "NW"}

    fb = guess_feedback(feature, feature)
    assert fb["correct"] is True
    assert "Correct" in format_feedback(fb)

    print("All Worldle checks passed.")


if __name__ == "__main__":
    run_checks()
