from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chwplantfulltest.io import load_csv_data
from chwplantfulltest.metrics import calculate_generic_kpi, save_kpi_results
from chwplantfulltest.scenarios import load_platform_config
from chwplantfulltest.simulation import PlatformSimulation


def main():
    config = load_platform_config(ROOT / "configs" / "sensor_bias.yaml")
    sim = PlatformSimulation(config)
    sim.initialize()
    results = sim.run()
    csv_data = load_csv_data(sim.csv_filename)
    kpi = calculate_generic_kpi(results, csv_data, sim)
    kpi["_controller_name"] = "Default_RBC_TChiBias"
    save_kpi_results(kpi, sim.results_dir, sim.timestamp)
    print(f"Completed sensor-bias RBC example. Results: {sim.csv_filename}")


if __name__ == "__main__":
    main()
