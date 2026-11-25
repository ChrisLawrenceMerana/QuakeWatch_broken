# Repair log

Study group: ______________________   Members: ______________________________________________

## Defects

| # | Symptom (what was wrong for the user) | Cause (file, function, line; why it was wrong) | Fix (what you changed) | Test that now guards it | Fixed by |
| --- | --- | --- | --- | --- | --- |
| 1 | `python run.py` stops with a `KeyError` before the dashboard is written. | `quakewatch.py`, `features_stage()`: `depth_class(t["depth"])` used a column that does not exist. The real column is `depth_km` (set in `features_to_table()`). pandas raised `KeyError: 'depth'` after acquire and integrate, before `report()`. | Changed it to `depth_class(t["depth_km"])`. | `test_features_stage_reads_depth_km` in `tests/test_group.py` | Sheryl Jane E. Galleto |
| 2 | The dashboard says the strongest earthquake struck at 14:37 Manila time on 2 December 2023. The news reported it at 10:37 PM. | `quakewatch.py`, `features_stage()`: `t["time"].dt.tz_localize(None).dt.tz_localize("Asia/Manila")` relabelled the UTC clock time as Manila time instead of converting it, so every local time was 8 hours early (UTC+8). | Changed it to `t["time"].dt.tz_convert("Asia/Manila")`. | `test_manila_timezone_conversion` in `tests/test_group.py` | Macie L. Moises |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| test_features_stage_reads_depth_km | monkeypatch (fake data folder) | features_stage reads `depth_km` and gives shallow, intermediate and deep classes | Yes | Sheryl Jane E. Galleto |
| | | | | |
| | | | | |

## Logging we added

| Where (function) | Level | Message | Why this level |
| --- | --- | --- | --- |
| | | | |
| | | | |
| | | | |

## One thing we learned about debugging

(two or three sentences)
