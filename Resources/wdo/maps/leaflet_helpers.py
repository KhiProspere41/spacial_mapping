from ipyleaflet import Map, GeoJSON, basemaps
from wdo.geometry.bbox import bbox_from_feature


def make_map(center=(0, 0), zoom=2, basemap=None, scroll_wheel_zoom=True):
    """
    Return an ipyleaflet Map with useful defaults for Worldle.
    """
    if basemap is None:
        basemap = basemaps.OpenStreetMap.Mapnik

    return Map(
        center=center,
        zoom=zoom,
        basemap=basemap,
        scroll_wheel_zoom=scroll_wheel_zoom,
    )


def add_geojson(map_obj, data, style=None, name="GeoJSON Layer"):
    """
    Add a GeoJSON layer to an ipyleaflet map and return the layer.
    """
    if style is None:
        style = {
            "color": "#222222",
            "fillColor": "#4f8cff",
            "weight": 2,
            "fillOpacity": 0.55,
        }

    layer = GeoJSON(
        data=data,
        style=style,
        name=name,
    )

    map_obj.add_layer(layer)
    return layer


def fit_map_to_geojson(map_obj, data):
    """
    Fit the map view to a GeoJSON Feature or FeatureCollection.
    """
    if data["type"] == "Feature":
        features = [data]
    elif data["type"] == "FeatureCollection":
        features = data["features"]
    else:
        raise ValueError("Expected a GeoJSON Feature or FeatureCollection")

    boxes = [bbox_from_feature(feature) for feature in features]

    min_lon = min(box[0] for box in boxes)
    min_lat = min(box[1] for box in boxes)
    max_lon = max(box[2] for box in boxes)
    max_lat = max(box[3] for box in boxes)

    map_obj.fit_bounds([
        [min_lat, min_lon],
        [max_lat, max_lon],
    ])

    return min_lon, min_lat, max_lon, max_lat