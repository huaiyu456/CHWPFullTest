from pathlib import Path
import argparse
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chwplantfulltest.io import load_csv_data
from chwplantfulltest.kpi.generic_kpi import calculate_generic_kpi
from chwplantfulltest.metrics import calculate_ftc_kpi, save_kpi_results


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-csv", required=True)
    parser.add_argument("--faulty-csv", required=True)
    parser.add_argument("--name", default="Default_RBC_FTC")
    parser.add_argument("--output-dir", default="results")
    return parser


def _results_from_csv(csv_data):
    return {
        "time": [row["EndTime"] for row in csv_data],
        "computation_time": [row.get("ComputationTime", 0.0) for row in csv_data],
    }


def main():
    args = build_parser().parse_args()
    baseline_csv = load_csv_data(args.baseline_csv)
    faulty_csv = load_csv_data(args.faulty_csv)
    baseline_kpi = calculate_generic_kpi(_results_from_csv(baseline_csv), baseline_csv)
    faulty_kpi = calculate_generic_kpi(_results_from_csv(faulty_csv), faulty_csv)
    ftc_kpi = calculate_ftc_kpi(baseline_kpi, faulty_kpi, baseline_csv, faulty_csv)
    ftc_kpi["_controller_name"] = args.name
    save_kpi_results(ftc_kpi, ROOT / args.output_dir, "comparison")
    print(f"Completed FTC KPI comparison. Output directory: {ROOT / args.output_dir}")


if __name__ == "__main__":
    main()
