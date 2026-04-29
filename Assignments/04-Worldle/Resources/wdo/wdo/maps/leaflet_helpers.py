"""Small ipyleaflet helpers used by Worldle."""

from __future__ import annotations

from ipyleaflet import GeoJSON, Map, basemaps

from wdo.geometry.bbox import bbox_from_feature


DEFAULT_STYLE = {
    "color": "#2b2d42",
    "fillColor": "#8ecae6",
    "weight": 2,
    "fillOpacity": 0.6,
}


def make_map(center: tuple[float, float] = (0, 0), zoom: int = 2, basemap=None, scroll_wheel_zoom: bool = True) -> Map:
    """Return an ipyleaflet Map with sensible Worldle defaults."""
    chosen_basemap = basemap if basemap is not None else basemaps.CartoDB.Positron
    return Map(center=center, zoom=zoom, basemap=chosen_basemap, scroll_wheel_zoom=scroll_wheel_zoom)


def add_geojson(map_obj: Map, data: dict, style: dict | None = None) -> GeoJSON:
    """Add GeoJSON data to map and return the created layer."""
    layer = GeoJSON(data=data, style=style or DEFAULT_STYLE)
    map_obj.add(layer)
    return layer


def fit_map_to_geojson(map_obj: Map, data: dict) -> tuple[float, float, float, float]:
    """Fit map bounds to GeoJSON feature or FeatureCollection and return the bbox used."""
    if data.get("type") == "FeatureCollection":
        features = data.get("features", [])
    elif data.get("type") == "Feature":
        features = [data]
    else:
        raise ValueError("Expected Feature or FeatureCollection")

    if not features:
        raise ValueError("GeoJSON contains no features")

    bboxes = [bbox_from_feature(feature) for feature in features]
    min_lon = min(b[0] for b in bboxes)
    min_lat = min(b[1] for b in bboxes)
    max_lon = max(b[2] for b in bboxes)
    max_lat = max(b[3] for b in bboxes)

    map_obj.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])
    return (min_lon, min_lat, max_lon, max_lat)
