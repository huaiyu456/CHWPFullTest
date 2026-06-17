import argparse

from chwplantfulltest.io import load_csv_data
from chwplantfulltest.simulation import PlatformSimulation
from chwplantfulltest.metrics import calculate_generic_kpi, save_kpi_results
from chwplantfulltest.scenarios import load_platform_config


# Defaults for direct execution.
# Command-line arguments can override these values.
DEFAULT_CONTROLLER = "Default_RBC"
DEFAULT_MODE = "test"
DEFAULT_CONFIG = "configs/fault_free.yaml"


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--controller", default=DEFAULT_CONTROLLER, choices=["Default_RBC"])
    parser.add_argument("--mode", default=DEFAULT_MODE, choices=["train", "test"])
    parser.add_argument("--controller-module", default=None)
    parser.add_argument("--controller-class", default=None)
    parser.add_argument("--controller-path", default=None)
    return parser


def main():
    args = build_parser().parse_args()
    config = load_platform_config(args.config)
    config.controller_type = args.controller
    config.controller_mode = args.mode
    if args.controller_module:
        config.controller_module = args.controller_module
    if args.controller_class:
        config.controller_class = args.controller_class
    if args.controller_path:
        config.controller_path = args.controller_path
    sim = PlatformSimulation(config)
    sim.initialize()
    results = sim.run()
    csv_data = load_csv_data(sim.csv_filename)
    kpi_results = calculate_generic_kpi(results, csv_data, sim)
    kpi_results["_controller_name"] = args.controller
    save_kpi_results(kpi_results, sim.results_dir, sim.timestamp)


if __name__ == "__main__":
    main()


