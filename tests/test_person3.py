from app.core.search_routes import haversine
import math

def test_haversine():
    # Test distance between Paris and London (approx 344 km)
    dist = haversine(48.8566, 2.3522, 51.5074, -0.1278)
    assert math.isclose(dist, 344.0, abs_tol=5.0)

    # Same point should be 0
    dist_zero = haversine(48.8566, 2.3522, 48.8566, 2.3522)
    assert dist_zero == 0.0
