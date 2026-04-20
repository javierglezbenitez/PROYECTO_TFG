from __future__ import annotations
import json
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any, List
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.config.config_loader import load_config


PER_PAGE = 200
RATE_COOLDOWN = 0.6
MAX_RETRIES = 3
FLICKR_METHOD = "flickr.photos.search"
#MAX_FOTOS_POR_MES = 100


def _parse_date(date_str: str) -> datetime:
    if date_str.lower() == "today":
        now = datetime.now()
        return datetime(now.year, now.month, now.day)
    return datetime.strptime(date_str, "%Y-%m-%d")

def _iter_monthly_windows(start: datetime, end: datetime):
    cursor = datetime(start.year, start.month, 1)
    while cursor <= end:
        next_month = (cursor.replace(day=28) + timedelta(days=4)).replace(day=1)
        yield int(cursor.timestamp()), int(next_month.timestamp()), cursor
        cursor = next_month

def _call_flickr(url: str, params: Dict[str, Any]):
    for attempt in range(MAX_RETRIES):
        time.sleep(RATE_COOLDOWN)
        try:
            resp = requests.get(url, params=params, timeout=15)
        except Exception:
            time.sleep(1)
            continue

        if resp.status_code == 200:
            try:
                return resp.json()
            except:
                return None

        if resp.status_code in (429, 500, 502, 503, 504):
            time.sleep(2 ** attempt)
            continue

        return None

    return None


def _search_month_limited(url, base_params, lat, lon, radius, min_ts, max_ts):
    results = []
    page = 1

    while True:
        params = {
            **base_params,
            "lat": lat,
            "lon": lon,
            "radius": radius,
            "radius_units": "km",
            "min_taken_date": min_ts,
            "max_taken_date": max_ts,
            "page": page,
        }

        data = _call_flickr(url, params)
        if not data or "photos" not in data:
            break

        photos = data["photos"]
        items = photos.get("photo", [])

        if not items:
            break

        for item in items:
            results.append(item)
            #if len(results) >= MAX_FOTOS_POR_MES:
            #    return results

        if page >= int(photos.get("pages", 1)):
            break

        page += 1

    return results

def get_photos_for_config_location(loc, config, out_dir=None) -> Path:
    url = config["URL"]
    api_key = config["credenciales_api"]["api_key"]
    extras = ",".join([e.strip() for e in config["extras"].split(",")])

    carpeta = out_dir if out_dir else config["carpeta"]
    path_out = Path(carpeta)
    path_out.mkdir(parents=True, exist_ok=True)

    start = _parse_date("2021-01-01")
    end = _parse_date(config["date_range"]["end_date"])

    base_params = {
        "method": FLICKR_METHOD,
        "api_key": api_key,
        "format": "json",
        "nojsoncallback": 1,
        "extras": extras,
        "per_page": PER_PAGE,
    }

    nombre = loc["nombre_zona"]
    lat = float(loc["lat"])
    lon = float(loc["lon"])
    radius = float(loc["radius"])

    print(f"\n=== Descargando isla: {nombre} ===")

    all_items = []

    for min_ts, max_ts, cursor in _iter_monthly_windows(start, end):
        etiqueta = cursor.strftime("%Y-%m")
        print(f"  · Mes {etiqueta}")
        #print(f"  · Mes {etiqueta} (máx {MAX_FOTOS_POR_MES})")

        mes_items = _search_month_limited(url, base_params, lat, lon, radius, min_ts, max_ts)
        print(f"    - Descargadas: {len(mes_items)}")

        all_items.extend(mes_items)

    out_file = path_out / f"{nombre}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_items, f, ensure_ascii=False, indent=2)

    print(f"[OK] {nombre}: {len(all_items)} fotos → {out_file}")
    return out_file


def download_all_from_yaml(config_path="configs/config.yaml", out_dir=None):
    config = load_config(config_path)
    locations = config.get("locations", [])

    if not locations:
        raise RuntimeError("ERROR: config.yaml no contiene 'locations'.")

    print("\n=== Descargando TODAS LAS ISLAS EN PARALELO ===\n")

    futures = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        for loc in locations:
            futures.append(executor.submit(get_photos_for_config_location, loc, config, out_dir))
        for task in as_completed(futures):
            task.result()
    print("\n✔ Descarga completa de Canarias\n")