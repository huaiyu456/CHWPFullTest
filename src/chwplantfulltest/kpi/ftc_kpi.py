import math
import re
from typing import Dict, List

import numpy as np


def _metric_value(value):
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", str(value))
    if not match:
        return math.nan
    return float(match.group(0))


def calculate_ftc_kpi(
    baseline_kpi: Dict[str, str],
    faulty_kpi: Dict[str, str],
    baseline_csv: List[dict],
    faulty_csv: List[dict],
) -> Dict[str, str]:
    ftc = {}
    comparable_keys = [
        "Discomfort hours (DH)",
        "Discomfort degree hours (DDH)",
        "Peak discomfort degree",
        "Cycle Energy Consumption",
        "Peak energy consumption",
        "Cycle energy consumption cost",
        "Calculation time ratio",
    ]

    for key in comparable_keys:
        base = _metric_value(baseline_kpi.get(key, math.nan))
        fault = _metric_value(faulty_kpi.get(key, math.nan))
        if math.isnan(base) or math.isnan(fault):
            continue
        diff = fault - base
        if abs(base) > 1e-12:
            ftc[f"{key} degradation"] = f"{diff:.6g}"
            ftc[f"{key} degradation ratio"] = f"{diff / base * 100:.2f} %"
        else:
            ftc[f"{key} degradation"] = f"{diff:.6g}"
            ftc[f"{key} degradation ratio"] = "NA (baseline is zero)"

    base_tair = np.array([row["TAirSup.T"] for row in baseline_csv], dtype=float) - 273.15
    fault_tair = np.array([row["TAirSup.T"] for row in faulty_csv], dtype=float) - 273.15
    n = min(len(base_tair), len(fault_tair))
    if n > 0:
        diff_tair = fault_tair[:n] - base_tair[:n]
        ftc["Mean supply-air temperature deviation"] = f"{np.mean(diff_tair):.4f} K"
        ftc["Max absolute supply-air temperature deviation"] = f"{np.max(np.abs(diff_tair)):.4f} K"

    base_power = np.array([row["PAll1.y"] for row in baseline_csv], dtype=float)
    fault_power = np.array([row["PAll1.y"] for row in faulty_csv], dtype=float)
    n = min(len(base_power), len(fault_power))
    if n > 0:
        diff_power = fault_power[:n] - base_power[:n]
        ftc["Mean power deviation"] = f"{np.mean(diff_power) / 1000:.4f} kW"
        ftc["Max absolute power deviation"] = f"{np.max(np.abs(diff_power)) / 1000:.4f} kW"

    return ftc
