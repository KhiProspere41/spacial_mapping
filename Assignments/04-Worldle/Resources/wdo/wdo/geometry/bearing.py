"""Bearing helpers for lon/lat coordinates."""

from __future__ import annotations

import math

COMPASS_8 = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]


def initial_bearing(p1: tuple[float, float], p2: tuple[float, float]) -> float:
    """Return initial bearing in degrees from p1 to p2.

    Points are in (lat, lon) order.
    """
    lat1, lon1 = map(math.radians, p1)
    lat2, lon2 = map(math.radians, p2)

    d_lon = lon2 - lon1
    x = math.sin(d_lon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(d_lon)

    bearing = math.degrees(math.atan2(x, y))
    return (bearing + 360.0) % 360.0


def bearing_to_compass(bearing_deg: float) -> str:
    """Convert a numeric bearing to 8-point compass text."""
    idx = int((bearing_deg + 22.5) // 45) % 8
    return COMPASS_8[idx]
