"""Bounding-box helpers for GeoJSON features."""

from __future__ import annotations


def _coords_from_polygon(polygon_coords: list) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for ring in polygon_coords:
        for lon, lat in ring:
            points.append((lon, lat))
    return points


def bbox_from_feature(feature: dict) -> tuple[float, float, float, float]:
    """Return (min_lon, min_lat, max_lon, max_lat) for Polygon or MultiPolygon."""
    geometry = feature.get("geometry", {})
    geom_type = geometry.get("type")
    coords = geometry.get("coordinates", [])

    points: list[tuple[float, float]] = []
    if geom_type == "Polygon":
        points = _coords_from_polygon(coords)
    elif geom_type == "MultiPolygon":
        for poly in coords:
            points.extend(_coords_from_polygon(poly))
    else:
        raise ValueError(f"Unsupported geometry type for bbox_from_feature: {geom_type}")

    if not points:
        raise ValueError("Feature has no coordinates")

    lons = [p[0] for p in points]
    lats = [p[1] for p in points]
    return (min(lons), min(lats), max(lons), max(lats))
