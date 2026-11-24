import pandas as pd

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