# Repair log

Study group: ______________________   Members: ______________________________________________

## Defects

| # | Symptom (what was wrong for the user) | Cause (file, function, line; why it was wrong) | Fix (what you changed) | Test that now guards it | Fixed by |
| --- | --- | --- | --- | --- | --- |
| 1 | `python run.py` stops with a `KeyError` before the dashboard is written. | `quakewatch.py`, `features_stage()`: `depth_class(t["depth"])` used a column that does not exist. The real column is `depth_km` (set in `features_to_table()`). pandas raised `KeyError: 'depth'` after acquire and integrate, before `report()`. | Changed it to `depth_class(t["depth_km"])`. | `test_features_stage_reads_depth_km` in `tests/test_group.py` | Sheryl Jane E. Galleto |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| test_features_stage_reads_depth_km | monkeypatch (fake data folder) | features_stage reads `depth_km` and gives shallow, intermediate and deep classes | Not checked yet | Sheryl Jane E. Galleto |
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
