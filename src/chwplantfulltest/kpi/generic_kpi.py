import numpy as np
from datetime import datetime, timedelta

BASE_DATETIME = datetime(2020, 1, 1)


def get_electricity_price(timestamp):
    dt = BASE_DATETIME + timedelta(seconds=timestamp)
    hour = dt.hour
    if (10 <= hour < 12) or (14 <= hour < 19):
        return 1.0794
    elif (8 <= hour < 10) or (12 <= hour < 14) or (19 <= hour < 24):
        return 0.6542
    else:
        return 0.3271


def calculate_time_in_price_ranges(start_ts, end_ts):
    PRICE_PEAK = 1.0794
    PRICE_FLAT = 0.6542
    PRICE_VALLEY = 0.3271
    time_in_ranges = {PRICE_PEAK: 0.0, PRICE_FLAT: 0.0, PRICE_VALLEY: 0.0}
    current_ts = start_ts
    while current_ts < end_ts:
        current_dt = BASE_DATETIME + timedelta(seconds=current_ts)
        next_hour = current_dt.hour + 1
        if next_hour == 24:
            next_day_dt = current_dt + timedelta(days=1)
            next_hour_dt = datetime(next_day_dt.year, next_day_dt.month, next_day_dt.day, 0, 0, 0)
        else:
            next_hour_dt = datetime(current_dt.year, current_dt.month, current_dt.day, next_hour, 0, 0)
        next_hour_ts = (next_hour_dt - BASE_DATETIME).total_seconds()
        period_end_ts = min(next_hour_ts, end_ts)
        price = get_electricity_price(current_ts)
        duration_hours = (period_end_ts - current_ts) / 3600
        time_in_ranges[price] += duration_hours
        current_ts = period_end_ts
    return time_in_ranges


def calculate_generic_kpi(results, csv_data, simulation=None):
    kpi = {}
    timestamps = np.array([row["EndTime"] for row in csv_data])
    step_durations = np.diff(timestamps) / 3600
    step_durations = np.concatenate([[0], step_durations])
    ta_air_sup = np.array([row["TAirSup.T"] - 273.15 for row in csv_data])
    dh = np.sum(np.where(ta_air_sup > 27.5, step_durations, 0))
    kpi["Discomfort hours (DH)"] = f"{dh:.2f} h"
    ddh_values = np.where(ta_air_sup > 27.5, (ta_air_sup - 27.5) * step_durations, 0)
    kpi["Discomfort degree hours (DDH)"] = f"{np.sum(ddh_values):.2f} K*h"
    sorted_ta = np.sort(ta_air_sup)[::-1]
    top_percent_idx = max(1, int(len(sorted_ta) * 0.00579))
    top_avg = np.mean(sorted_ta[:top_percent_idx])
    kpi["Peak discomfort degree"] = f"{max(0.0, top_avg - 27.5):.2f} K"
    cycle_energy = csv_data[-1]["EnergyAgg.y"]
    kpi["Cycle Energy Consumption"] = f"{cycle_energy:.2f} kWh"
    p_all1 = np.array([row["PAll1.y"] for row in csv_data])
    kpi["Peak energy consumption"] = f"{np.max(p_all1) / 1000:.2f} kW"
    total_cost = 0.0
    price_stats = {1.0794: {"hours": 0.0, "energy": 0.0}, 0.6542: {"hours": 0.0, "energy": 0.0}, 0.3271: {"hours": 0.0, "energy": 0.0}}
    for i in range(1, len(csv_data)):
        start_ts = csv_data[i - 1]["EndTime"]
        end_ts = csv_data[i]["EndTime"]
        duration_hours = (end_ts - start_ts) / 3600
        if duration_hours <= 0:
            continue
        energy_diff = csv_data[i]["EnergyAgg.y"] - csv_data[i - 1]["EnergyAgg.y"]
        energy_per_hour = energy_diff / duration_hours if duration_hours > 0 else 0
        time_ranges = calculate_time_in_price_ranges(start_ts, end_ts)
        for price, hours in time_ranges.items():
            if hours <= 0:
                continue
            range_energy = energy_per_hour * hours
            price_stats[price]["hours"] += hours
            price_stats[price]["energy"] += range_energy
            total_cost += range_energy * price
    kpi["Cycle energy consumption cost"] = f"{total_cost:.2f}"
    kpi["Price tier statistics"] = (
        f"Peak: {price_stats[1.0794]['hours']:.2f}h, {price_stats[1.0794]['energy']:.2f}kWh; "
        f"Flat: {price_stats[0.6542]['hours']:.2f}h, {price_stats[0.6542]['energy']:.2f}kWh; "
        f"Valley: {price_stats[0.3271]['hours']:.2f}h, {price_stats[0.3271]['energy']:.2f}kWh"
    )
    total_comp_time = np.sum(results["computation_time"])
    sim_total_time = results["time"][-1] - results["time"][0]
    comp_ratio = total_comp_time / sim_total_time if sim_total_time != 0 else 0
    kpi["Calculation time ratio"] = f"{comp_ratio:.6f} (ratio)"
    return kpi



