from download import save_json
from stats import summarize_weather
import json
import pathlib
import math

BASE_DIR = pathlib.Path(__file__).resolve().parent


def test_save_json():
    path = pathlib.Path("weather.json")
    if path.exists():
        path.unlink()
    save_json(38.9, -77.1, 7)
    data = json.loads(path.read_text())
    assert 38.9 <= data["latitude"] <= 39
    assert -77.1 <= data["longitude"] <= -77
    assert len(data["daily"]["time"]) in (7, 8)


def test_stats_dates():
    summary = summarize_weather(BASE_DIR / "test-weather.json")
    assert summary["start_date"] == "2022-11-08"
    assert summary["end_date"] == "2022-11-15"


def test_stats_meanhigh():
    summary = summarize_weather(BASE_DIR / "test-weather.json")
    assert math.isclose(summary["mean_high"], 15.233333333)


def test_stats_meanlow():
    summary = summarize_weather(BASE_DIR / "test-weather.json")
    assert math.isclose(summary["mean_low"], 5.5333333333)


def test_stats_max():
    summary = summarize_weather(BASE_DIR / "test-weather.json")
    assert math.isclose(summary["max_high"], 15.9)


def test_stats_min():
    summary = summarize_weather(BASE_DIR / "test-weather.json")
    assert math.isclose(summary["min_low"], 3.8)


def test_stats_stdhigh():
    summary = summarize_weather(BASE_DIR / "test-weather.json")
    assert math.isclose(summary["std_dev_high"], 0.6110100926607792)


def test_stats_stdlow():
    summary = summarize_weather(BASE_DIR / "test-weather.json")
    assert math.isclose(summary["std_dev_low"], 2.500666577801)
