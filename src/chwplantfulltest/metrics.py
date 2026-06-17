import csv
import os
from datetime import datetime, timedelta
import numpy as np

BASE_DATETIME = datetime(2020, 1, 1)


def get_electricity_price(timestamp):
    dt = BASE_DATETIME + timedelta(seconds=timestamp)
    hour = dt.hour
    if (10 <= hour < 12) or (14 <= hour < 19):
        return 1.0794
    if (8 <= hour < 10) or (12 <= hour < 14) or (19 <= hour < 24):
        return 0.6542
    return 0.3271


def calculate_generic_kpi(results, csv_data, simulation=None):
    from chwplantfulltest.kpi.generic_kpi import calculate_generic_kpi as original
    return original(results, csv_data, simulation)


def calculate_ftc_kpi(baseline_kpi, faulty_kpi, baseline_csv, faulty_csv):
    from chwplantfulltest.kpi.ftc_kpi import calculate_ftc_kpi as original
    return original(baseline_kpi, faulty_kpi, baseline_csv, faulty_csv)


def save_kpi_results(kpi_results, save_dir, timestamp):
    os.makedirs(save_dir, exist_ok=True)
    controller_name = kpi_results.get("_controller_name", "Unknown")
    txt_filename = os.path.join(save_dir, f"{controller_name}_KPI_results_{timestamp}.txt")
    csv_filename = os.path.join(save_dir, f"{controller_name}_KPI_results_{timestamp}.csv")

    with open(txt_filename, "w", encoding="utf-8") as f:
        for name, value in kpi_results.items():
            if name == "_controller_name":
                continue
            f.write(f"{name}: {value}\n")

    with open(csv_filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Indicator", "Value"])
        for name, value in kpi_results.items():
            if name == "_controller_name":
                continue
            writer.writerow([name, value])


