"""Distance and direction utilities for Worldle."""

from __future__ import annotations

import math

EARTH_RADIUS_KM = 6371.0088
COMPASS_8 = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return great-circle distance in kilometers between two lat/lon points."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c


def initial_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return initial bearing in degrees from first point to second point."""
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    lam1 = math.radians(lon1)
    lam2 = math.radians(lon2)

    y = math.sin(lam2 - lam1) * math.cos(phi2)
    x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(lam2 - lam1)
    return (math.degrees(math.atan2(y, x)) + 360.0) % 360.0


def bearing_to_compass(bearing: float) -> str:
    """Convert a bearing in degrees into an 8-point compass direction."""
    idx = int((bearing + 22.5) // 45) % 8
    return COMPASS_8[idx]
