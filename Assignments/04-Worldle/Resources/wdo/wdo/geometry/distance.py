"""Distance helpers for lon/lat coordinates."""

from __future__ import annotations

import math

EARTH_RADIUS_KM = 6371.0088
KM_TO_MILES = 0.621371


def haversine_km(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Return great-circle distance in kilometers between two points.

    Points are in (lat, lon) order.
    """
    lat1, lon1 = p1
    lat2, lon2 = p2

    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return EARTH_RADIUS_KM * c


def haversine_miles(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Return great-circle distance in miles between two points."""
    return haversine_km(p1, p2) * KM_TO_MILES
