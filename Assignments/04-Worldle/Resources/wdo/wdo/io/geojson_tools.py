"""Simple GeoJSON loading helpers for class assignments."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator


def load_geojson(path: str | Path) -> dict[str, Any]:
    """Load and return a GeoJSON dictionary from disk."""
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def iter_features(geojson_obj: dict[str, Any]) -> Iterator[dict[str, Any]]:
    """Yield each feature from a GeoJSON FeatureCollection."""
    for feature in geojson_obj.get("features", []):
        yield feature
