"""Bounding box utilities for GeoJSON features."""

from __future__ import annotations


def _flatten_coords(coords, geometry_type: str):
    """Return a flat list of (lon, lat) tuples for a GeoJSON geometry type."""
    points = []

    if geometry_type == "Point":
        lon, lat = coords
        return [(lon, lat)]

    if geometry_type in {"MultiPoint", "LineString"}:
        return [(lon, lat) for lon, lat in coords]

    if geometry_type in {"MultiLineString", "Polygon"}:
        for part in coords:
            for lon, lat in part:
                points.append((lon, lat))
        return points

    if geometry_type == "MultiPolygon":
        for polygon in coords:
            for ring in polygon:
                for lon, lat in ring:
                    points.append((lon, lat))
        return points

    raise ValueError(f"Unsupported geometry type: {geometry_type}")


def bbox_from_feature(feature: dict) -> tuple[float, float, float, float]:
    """Return (min_lon, min_lat, max_lon, max_lat) for a GeoJSON feature."""
    geometry = feature.get("geometry") or {}
    geometry_type = geometry.get("type")
    coords = geometry.get("coordinates")

    if not geometry_type or coords is None:
        raise ValueError("Feature must contain geometry.type and geometry.coordinates")

    points = _flatten_coords(coords, geometry_type)
    if not points:
        raise ValueError("Feature has no coordinate points")

    lons = [lon for lon, _ in points]
    lats = [lat for _, lat in points]
    return (min(lons), min(lats), max(lons), max(lats))
