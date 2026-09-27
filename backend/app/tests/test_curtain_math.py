from app.engines.curtain_math import fabric_meters
import pytest

def test_living_room():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4)
    assert r["panels"] == 5
    assert r["cut_height"] == 2.85
    assert r["meters"] == 14.25
    assert r["bay_depth"] == 0.0

def test_single_panel_narrow():
    r = fabric_meters(1.0, 2.0, 1.5, 0.0, 0.0, 2.8)
    assert r["panels"] == 1
    assert r["meters"] == 2.0

def test_bay_depth_extends_cut_height():
    r = fabric_meters(3.0, 2.6, 2.0, 0.10, 0.15, 1.4, bay_depth=0.6)
    assert r["panels"] == 5
    assert r["cut_height"] == 3.45
    assert r["meters"] == 17.25
    assert r["bay_depth"] == 0.6

def test_bay_depth_zero_matches_base():
    assert fabric_meters(2.2, 1.5, 2.0, 0.10, 0.15, 1.4, bay_depth=0.0) == \
           fabric_meters(2.2, 1.5, 2.0, 0.10, 0.15, 1.4)

def test_negative_bay_depth_rejected():
    with pytest.raises(ValueError):
        fabric_meters(2.2, 1.5, 2.0, 0.10, 0.15, 1.4, bay_depth=-0.1)
