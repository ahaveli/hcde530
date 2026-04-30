"""Fetch current weather for Seattle via OpenWeatherMap (API key in .env as OPENWEATHERMAP_API_KEY)."""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

WEATHER_BASE = "https://api.openweathermap.org/data/2.5/weather"
# Seattle, US — OpenWeather “City name, state, country” works well for the US
DEFAULT_QUERY = "Seattle,WA,US"
UNITS = "imperial"  # °F, mph; use "metric" for °C, m/s

_ENV_PATH = Path(__file__).resolve().parent / ".env"


def _load_env_file() -> None:
    """Set os.environ from KEY=value lines in .env (does not override already-set env vars)."""
    if not _ENV_PATH.is_file():
        return
    for raw in _ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key, value = key.strip(), value.strip()
        if not key or key in os.environ:
            continue
        if len(value) >= 2 and value[0] == value[-1] and value[0] in '\'"':
            value = value[1:-1]
        os.environ[key] = value


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def fetch_seattle_weather(api_key: str, city: str = DEFAULT_QUERY) -> dict:
    """GET current weather; see https://openweathermap.org/current."""
    q = urllib.parse.urlencode(
        {
            "q": city,
            "appid": api_key,
            "units": UNITS,
        }
    )
    return _get_json(f"{WEATHER_BASE}?{q}")


def _format_output(data: dict) -> str:
    name = data.get("name", "Unknown")
    main = data.get("main", {})
    weather = (data.get("weather") or [{}])[0]
    desc = str(weather.get("description", "")).title()
    wind = data.get("wind") or {}
    u = "°F" if UNITS == "imperial" else "°C"
    wu = "mph" if UNITS == "imperial" else "m/s"
    temp = main.get("temp")
    feels = main.get("feels_like")
    humidity = main.get("humidity")
    speed = wind.get("speed")
    lines = [
        f"Current weather: {name}",
        f"  Conditions: {desc or 'N/A'}",
    ]
    if temp is not None and feels is not None:
        lines.append(f"  Temperature: {temp}{u} (feels like {feels}{u})")
    if humidity is not None:
        lines.append(f"  Humidity: {humidity}%")
    if speed is not None:
        lines.append(f"  Wind: {speed} {wu}")
    return "\n".join(lines)


def main() -> None:
    _load_env_file()
    key = os.environ.get("OPENWEATHERMAP_API_KEY", "").strip()
    if not key:
        print(
            "Missing OPENWEATHERMAP_API_KEY. Set it in .env in this folder or in your environment.",
            file=sys.stderr,
        )
        raise SystemExit(1)
    try:
        data = fetch_seattle_weather(key)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {err_body}", file=sys.stderr)
        raise SystemExit(1) from e
    except urllib.error.URLError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        raise SystemExit(1) from e
    print(_format_output(data))


if __name__ == "__main__":
    main()
