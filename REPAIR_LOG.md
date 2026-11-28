# Repair log

Study group: ______________________   Members: ______________________________________________

## Defects

| # | Symptom (what was wrong for the user) | Cause (file, function, line; why it was wrong) | Fix (what you changed) | Test that now guards it | Fixed by |
| --- | --- | --- | --- | --- | --- |
| 1 | `python run.py` stops with a `KeyError` before the dashboard is written. | `quakewatch.py`, `features_stage()`: `depth_class(t["depth"])` used a column that does not exist. The real column is `depth_km` (set in `features_to_table()`). pandas raised `KeyError: 'depth'` after acquire and integrate, before `report()`. | Changed it to `depth_class(t["depth_km"])`. | `test_features_stage_reads_depth_km` in `tests/test_group.py` | Sheryl Jane E. Galleto |
| 2 | The dashboard says the strongest earthquake struck at 14:37 Manila time on 2 December 2023. The news reported it at 10:37 PM. | `quakewatch.py`, `features_stage()`: `t["time"].dt.tz_localize(None).dt.tz_localize("Asia/Manila")` relabelled the UTC clock time as Manila time instead of converting it, so every local time was 8 hours early (UTC+8). | Changed it to `t["time"].dt.tz_convert("Asia/Manila")`. | `test_manila_timezone_conversion` in `tests/test_group.py` | Macie L. Moises |
| 3 | A magnitude 6.0 earthquake is labelled `Moderate` instead of `Strong`. | `quakewatch.py`, `MAG_BINS` (line 33): the second bin edge was `6.05` instead of `5.95`, placing `6.0` inside `(4.95, 6.05]` (`Moderate`). | Changed `MAG_BINS` second edge from `6.05` to `5.95` so `6.0`–`6.9` maps to `Strong`. | `test_features.py::test_strong_or_above_count` and `test_group.py::test_mag_class_strong_boundary` | Aljur Cabalfin |
| 4 | Earthquakes in mindanao are listed with a different location | The order of `longitude` and `latitude` in `nearest_city` are swapped, specifically for `events`| Swapped `latitude` and `longitude` for `events` | `test_correct_coordinates` | Clarence John D. Ello |
| 5 | `load_new` saves events that have already been saved as seen when running a second time| The function does not mark what has already been saved | `watermark()` was added in order for `load_new` to track saved files | `test_second_load_no_dupes`| Clarence John D. Ello |
| 6 | A row with depth -5 km is in the clean file, and the log says 0 rejected. | `quakewatch.py`, `split_by_contract()`: `except Exception: pass` hid the pandera error, and the function always returned every row as good with an empty rejects table. | Validate with `lazy=True`, read the failing row indexes from `failure_cases`, split into good and rejected rows, log a WARNING, and re-raise table-wide errors with `log.exception`. | `test_bad_rows_are_set_aside` in `tests/test_integrate.py`; `test_bad_depth_is_rejected_and_warned` and `test_depth_limits` in `tests/test_group.py` | ______ |

## Our own tests (in `tests/test_group.py`)

| Test name | Tool used (`parametrize`, fake API, `caplog`) | What it proves | Fails on the broken code? | Written by |
| --- | --- | --- | --- | --- |
| test_features_stage_reads_depth_km | monkeypatch (fake data folder) | features_stage reads `depth_km` and gives shallow, intermediate and deep classes | Yes | Sheryl Jane E. Galleto |
| test_manila_timezone_conversion | parametrize (3 cases), monkeypatch (fake data folder) | features_stage converts UTC to Manila time (UTC+8), including across midnight | Yes | Macie L. Moises |
| test_correct_coordinates | paramterize (2 cases) | nearest_city now uses latitude and longitude in the intended order | Yes | Clarence John D. Ello|
| test_second_load_no_dupes | monkeypatch(fake API), caplog | Loading a second time no longer saves again | Yes | Clarence John D. Ello |
| test_bad_depth_is_rejected_and_warned | caplog | A -5 km row is set aside, the good rows are kept, and a WARNING is logged | Yes | ______ |
| test_depth_limits | parametrize (4 cases) | Depth 0 and 700 are accepted; -0.1 and 700.1 are rejected | Yes | ______ |

## Logging we added

| Where (function) | Level | Message | Why this level |
| --- | --- | --- | --- |
| `split_by_contract` | WARNING | `integrate: N rows rejected by the contract` | Bad rows are set aside, so the pipeline can continue, but someone should look at them |
| `split_by_contract` | ERROR (`log.exception`) | `integrate: contract failed for the whole table` | A missing column or wrong type makes every row unusable; the error is re-raised with its traceback |
| `run.py` | INFO | all pipeline messages written to `logs/run.log` | Keeps a record of each run for the submission |

## One thing we learned about debugging

(two or three sentences)
