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


def bbox_from_feature(feature):
    """
    Return (min_lon, min_lat, max_lon, max_lat) for a GeoJSON Feature.
    Supports Polygon and MultiPolygon.
    """
    points = _coords_from_geometry(feature["geometry"])

    if not points:
        raise ValueError("No coordinates found in feature.")

    lons = [p[0] for p in points]
    lats = [p[1] for p in points]

    return min(lons), min(lats), max(lons), max(lats)