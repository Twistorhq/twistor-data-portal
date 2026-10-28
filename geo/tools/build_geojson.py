#!/usr/bin/env python3
"""Build the CLIMATESHIFT-1 map layer for the GeoLibre proof (TW-728).

Prepared by Twistor Holdings LLC

Runs the real CLIMATESHIFT-1 v1 hemp seed from lbt-os
(backend/app/data_layer/science/crop_climate/seed.py, TW-599) and emits
one GeoJSON feature per trial record (30 records). The seed records
carry named trial locations only, so each feature's geometry is the
documented city coordinate of the record's named location (the
extension program site named in the seed). Every measurement value in
the properties is the record's own value, unmodified. V1 rows are
synthetic and stay labeled synthetic=true, same as everywhere else on
the portal.

Usage:
    python3 build_geojson.py [path-to-lbt-os] [output.geojson]
Defaults: ~/workspace/repos/lbt-os and ../data/climateshift-1-hemp.geojson
relative to this script.
"""

from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import sys
import types
from pathlib import Path

# City coordinates (lon, lat) for the five named trial sites in the seed.
SITE_COORDS = {
    "Burlington, VT": (-73.2121, 44.4759),
    "Corvallis, OR": (-123.2620, 44.5646),
    "Columbia, MO": (-92.3341, 38.9517),
    "Ithaca, NY": (-76.5019, 42.4440),
    "Fort Collins, CO": (-105.0844, 40.5853),
}


def load_seed_module(lbt_os: Path):
    """Load crop_climate/seed.py with its relative models import stubbed.

    The seed functions return plain dicts and never touch models at
    runtime; the stub keeps this generator stdlib-only.
    """
    seed_path = (
        lbt_os
        / "backend/app/data_layer/science/crop_climate/seed.py"
    )
    pkg = types.ModuleType("cc_seed_pkg")
    pkg.__path__ = [str(seed_path.parent)]
    sys.modules["cc_seed_pkg"] = pkg
    sys.modules["cc_seed_pkg.models"] = types.ModuleType("models")
    loader = importlib.machinery.SourceFileLoader(
        "cc_seed_pkg.seed", str(seed_path)
    )
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[loader.name] = module
    loader.exec_module(module)
    return module


def main() -> int:
    here = Path(__file__).resolve().parent
    lbt_os = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
        "~/workspace/repos/lbt-os"
    ).expanduser()
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else (
        here.parent / "data" / "climateshift-1-hemp.geojson"
    )

    seed = load_seed_module(lbt_os)
    records = seed.seed_hemp_records()
    assert len(records) == 30, f"expected 30 hemp records, got {len(records)}"

    features = []
    for i, rec in enumerate(records):
        loc = rec["location"]
        lon, lat = SITE_COORDS[loc]
        traits = rec["traits"]
        weather = rec["weather"]
        cond = rec["conditions"]
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [lon, lat]},
                "properties": {
                    "record": i + 1,
                    "dataset": "CLIMATESHIFT-1",
                    "dataset_version": "1.0",
                    "synthetic": rec["synthetic"],
                    "location": loc,
                    "program": cond["program"],
                    "genotype": rec["genotype"],
                    "use_type": cond["use_type"],
                    "year": rec["year"],
                    "yield_t_ha": rec["yield_t_ha"],
                    "thc_pct": traits["thc_pct"],
                    "cbd_pct": traits["cbd_pct"],
                    "cbg_pct": traits["cbg_pct"],
                    "thc_compliant_03": traits["thc_compliant_03"],
                    "fiber_quality_grade": traits["fiber_quality_grade"],
                    "lab_accreditation_id": traits["lab_accreditation_id"],
                    "season_precip_mm": weather["season_precip_mm"],
                    "heat_days_gt35c": weather["heat_days_gt35c"],
                    "temp_anomaly_c": weather["temp_anomaly_c"],
                    "drought_index": weather["drought_index"],
                    "simulated_future_climate": bool(
                        cond.get("simulated_future_climate")
                    ),
                    "climate_scenario": cond.get("climate_scenario"),
                },
            }
        )

    collection = {
        "type": "FeatureCollection",
        "name": "CLIMATESHIFT-1 v1 hemp trial records",
        "properties": {
            "dataset": "CLIMATESHIFT-1",
            "version": "1.0",
            "synthetic": True,
            "source": "lbt-os crop_climate seed (TW-599), seed_hemp_records()",
            "geometry_note": (
                "Seed records carry named locations only; geometry is the "
                "city coordinate of each record's named trial location."
            ),
        },
        "features": features,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(collection, indent=1) + "\n")
    print(f"wrote {out} with {len(features)} features")

    # Self-contained GeoLibre project: blank basemap (no tile network
    # needed) with the same FeatureCollection embedded inline. Used for
    # offline review and for verifying the layer renders where external
    # tile CDNs are unreachable. Format per the app docs
    # (docs/project-format.md), format version 0.2.0.
    layer_id = "climateshift-1-hemp-records"
    style = {
        "minZoom": 0,
        "maxZoom": 24,
        "fillColor": "#4353ff",
        "strokeColor": "#232a6b",
        "strokeWidth": 2,
        "strokeWidthUnit": "pixels",
        "fillOpacity": 0.85,
        "circleRadius": 7,
    }
    project = {
        "version": "0.2.0",
        "name": "CLIMATESHIFT-1 trial sites (Twistor Data portal proof)",
        "mapView": {"center": [-96.5, 38.6], "zoom": 3, "bearing": 0, "pitch": 0},
        "basemapStyleUrl": "",
        "basemapVisible": True,
        "basemapOpacity": 1,
        "blankBackgroundColor": None,
        "layers": [
            {
                "id": layer_id,
                "name": "CLIMATESHIFT-1 hemp trial records",
                "type": "geojson",
                "source": {"type": "geojson"},
                "visible": True,
                "opacity": 1,
                "style": style,
                "metadata": {
                    "dataset": "CLIMATESHIFT-1 v1",
                    "synthetic": True,
                    "geometry_note": collection["properties"]["geometry_note"],
                    "source": "lbt-os crop_climate seed (TW-599); generated "
                    "by geo/tools/build_geojson.py",
                },
                "geojson": collection,
            }
        ],
        "selectedLayerId": layer_id,
        "styles": {layer_id: style},
        "metadata": {"prepared_by": "Twistor Holdings LLC", "ticket": "TW-728"},
    }
    project_path = out.parent / "climateshift-1-project.geolibre.json"
    project_path.write_text(json.dumps(project, indent=1) + "\n")
    print(f"wrote {project_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
