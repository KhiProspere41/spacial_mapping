"""Small ipyleaflet helpers used by the Worldle notebook."""

from __future__ import annotations

from ..geometry.bbox import bbox_from_feature


def _require_ipyleaflet():
    """Import ipyleaflet lazily and raise a helpful error if unavailable."""
    try:
        from ipyleaflet import GeoJSON, Map, basemaps
        return GeoJSON, Map, basemaps
    except ImportError as exc:
        raise ImportError(
            "ipyleaflet is required for map rendering. Install it with: pip install ipyleaflet"
        ) from exc


def make_map(center: tuple[float, float] = (20, 0), zoom: int = 2):
    """Create and return a world map with starter defaults."""
    _, Map, basemaps = _require_ipyleaflet()
    return Map(center=center, zoom=zoom, basemap=basemaps.CartoDB.Positron)


def add_geojson(map_obj, geojson_data: dict, name: str = "GeoJSON"):
    """Add GeoJSON data to a map and return the created layer."""
    GeoJSON, _, _ = _require_ipyleaflet()
    layer = GeoJSON(
        data=geojson_data,
        name=name,
        style={"color": "#1f77b4", "fillColor": "#8ecae6", "weight": 2, "fillOpacity": 0.6},
    )
    map_obj.add(layer)
    return layer


def fit_map_to_geojson(map_obj, geojson_data: dict):
    """Fit map view to a GeoJSON Feature or FeatureCollection."""
    gtype = geojson_data.get("type")
    if gtype == "FeatureCollection":
        features = geojson_data.get("features", [])
    elif gtype == "Feature":
        features = [geojson_data]
    else:
        raise ValueError("geojson_data must be a Feature or FeatureCollection")

    if not features:
        raise ValueError("geojson_data has no features to fit")

    boxes = [bbox_from_feature(f) for f in features]
    min_lon = min(b[0] for b in boxes)
    min_lat = min(b[1] for b in boxes)
    max_lon = max(b[2] for b in boxes)
    max_lat = max(b[3] for b in boxes)

    map_obj.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
    return (min_lon, min_lat, max_lon, max_lat)
