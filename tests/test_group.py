import pandas as pd
import pytest
import quakewatch as qw


def test_features_stage_reads_depth_km(tmp_path, monkeypatch):
    """Incident 1: features_stage used a column called 'depth' that does not exist."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(qw, "CLEAN", tmp_path / "data" / "clean")
    monkeypatch.setattr(qw, "FEAT", tmp_path / "data" / "features")
    (tmp_path / "data" / "clean").mkdir(parents=True)
    clean = pd.DataFrame({
        "id": ["a", "b", "c"],
        "time": pd.to_datetime(["2023-01-01", "2023-01-02", "2023-03-01"], utc=True),
        "depth_km": [10.0, 100.0, 400.0],
        "mag": [5.2, 6.5, 7.2],
    })
    clean.to_parquet(tmp_path / "data" / "clean" / "events.parquet", index=False)

    out = qw.features_stage()

    assert list(out["depth_class"]) == ["shallow", "intermediate", "deep"]


@pytest.mark.parametrize(
    "utc_iso, expected_hour, expected_str",
    [
        ("2023-12-02T14:37:00Z", 22, "02 Dec 2023 22:37"),
        ("2023-12-02T00:00:00Z", 8, "02 Dec 2023 08:00"),
        ("2023-12-02T16:00:00Z", 0, "03 Dec 2023 00:00"),
    ],
)
def test_manila_timezone_conversion(
    tmp_path, monkeypatch, utc_iso, expected_hour, expected_str
):
    """Incident 2: UTC times must be converted to Manila time (UTC+8), not relabelled."""
    clean_dir = tmp_path / "clean"
    feat_dir = tmp_path / "features"
    clean_dir.mkdir()

    events = pd.DataFrame(
        {
            "time": [pd.Timestamp(utc_iso)],
            "mag": [7.6],
            "depth_km": [10.0],
        }
    )
    events.to_parquet(clean_dir / "events.parquet", index=False)

    monkeypatch.setattr(qw, "CLEAN", clean_dir)
    monkeypatch.setattr(qw, "FEAT", feat_dir)

    result = qw.features_stage()

    assert str(result.loc[0, "local"].tz) == "Asia/Manila"
    assert int(result.loc[0, "hour_local"]) == expected_hour
    assert f"{result.loc[0, 'local']:%d %b %Y %H:%M}" == expected_str


@pytest.mark.parametrize(
    "mag, expected",
    [
        (5.9, "Moderate"),
        (6.0, "Strong"),
        (6.9, "Strong"),
        (7.0, "Major"),
    ],
)
def test_mag_class_strong_boundary(mag, expected):
    """Incident 3: magnitude 6.0 to 6.9 must be labelled Strong."""
    result = qw.mag_class(pd.Series([mag])).iloc[0]
    assert result == expected


@pytest.mark.parametrize("lat, lon, city_id", [
    (8.9, 126.4, "C10"), 
    (17.5, 121.8, "C04"),
])

def test_correct_coordinates(lat, lon, city_id):
    """Incident 4: latitude and longitude must not be swapped"""
    events = pd.DataFrame({"latitude": [lat], "longitude": [lon]})
    cities = pd.DataFrame({"city_id": ["C04", "C10"],
                           "latitude": [17.6132, 8.9475],
                           "longitude": [121.7270, 125.5406]})

    ids, _ = qw.correct_coordinates(events, cities)

    assert ids[0] == city_id