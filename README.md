# CHWPlantFullTest

CHWPlantFullTest is a Python-FMU virtual test platform for benchmarking chilled water plant control strategies under fault-free and faulty operating conditions. It provides an FMU-based plant emulator, programmable fault injection, a standardized controller interface, a built-in RBC baseline, and automated KPI reporting.

This public repository contains the cleaned, standalone platform implementation. Earlier internal v1/v2 development folders are not required for use and are not part of the public release.

## Public Release Scope

The core public platform is the tester itself. The built-in RBC behavior embedded in the FMU is the minimum runnable baseline and the only controller included in this public upload. External research controllers are not part of this release.

The platform is designed to support reproducible controller testing under configured scenarios. This public release focuses on the RBC baseline and the surrounding test infrastructure.

The repository supports two execution modes: local execution for development and Docker execution for reproducible deployment.

## Repository Structure

```text
CHWPlantFullTest/
  src/chwplantfulltest/        Platform Python package
    control/                   Controller interface and included controllers
    kpi/                       KPI calculations
    utils/                     FMU state and utility helpers
    simulation.py              Main FMU simulation loop
    config.py                  Programmatic platform configuration
  models/                      FMU model files
  weather/                     Weather files used by FMU scenarios
  configs/                     Example scenario configuration files
  examples/                    Runnable local examples
  docs/                        Platform documentation
  tests/                       Lightweight pytest tests
  results/                     Default output directory
```

## Installation

Python 3.10 is recommended. PyFMI is easiest to install from conda-forge:

```bash
conda create -n chwplantfulltest python=3.10
conda activate chwplantfulltest
conda install -c conda-forge pyfmi
pip install -r requirements.txt
```

The public release does not require TensorFlow or SciPy.

## Quick Start

### Local Execution

Run the default built-in RBC baseline under fault-free operation:

```bash
python examples/run_fault_free_rbc.py
```

Additional examples:

```bash
python examples/run_sensor_bias_rbc.py
python examples/run_pump_stuck_rbc.py
```

Outputs are written to `results/` as controller result CSV files and KPI summaries.

The default public example uses `models/DataCenterCHWP_HybridFault.fmu`. The included weather file is `weather/CHN_Guangdong.Shenzhen.594930_SWERA.mos`.

### Docker Execution

Build the image:

```bash
docker compose build
```

Run the default fault-free scenario:

```bash
docker compose run --rm chwplantfulltest --config configs/smoke_test.yaml
```

Run a fault scenario:

```bash
docker compose run --rm chwplantfulltest --config configs/sensor_bias.yaml
```

Docker writes outputs to the host `results/` directory. More Docker examples, including custom scenarios and user controllers, are provided in [docker_usage.md](docs/docker_usage.md).

## Scenario Configuration

The default settings for the example tests are defined by YAML files in `configs/`:

- `configs/fault_free.yaml`: fault-free baseline.
- `configs/sensor_bias.yaml`: chilled-water temperature sensor-bias fault.
- `configs/pump_stuck.yaml`: chilled-water pump-stuck fault.

Each example script loads its matching YAML file. For example, `examples/run_fault_free_rbc.py` loads `configs/fault_free.yaml`.

Scenario fields:

```yaml
name: fault_free
description: Built-in RBC baseline under fault-free operation.
controller: Default_RBC
mode: test
start_time: 0
step_size: 600
num_steps: 12
results_dir: results
faults: {}
```

- `start_time`: FMU simulation start time in seconds.
- `step_size`: control and simulation step size in seconds.
- `num_steps`: number of simulation steps.
- `results_dir`: output directory for result CSV and KPI files.
- `faults`: fault schedules keyed by FMU fault parameter name.
- `controller_path`, `controller_module`, `controller_class`: optional user controller loading fields.
- `controller_params`: optional dictionary passed to the controller.

You can also run the package runner with a selected scenario:

```bash
PYTHONPATH=src python -m chwplantfulltest.runner --config configs/fault_free.yaml
PYTHONPATH=src python -m chwplantfulltest.runner --config configs/sensor_bias.yaml
PYTHONPATH=src python -m chwplantfulltest.runner --config configs/pump_stuck.yaml
```

External controllers can be supplied without editing platform source code:

```bash
PYTHONPATH=src python -m chwplantfulltest.runner \
  --config configs/fault_free.yaml \
  --controller-module sample_controller \
  --controller-class SampleController \
  --controller-path user_controllers
```

## Fault Configuration

Fault-free operation is represented by an empty `faults` dictionary or by all fault parameters set to zero. A fault schedule is a list of `[fault_start_time_seconds, value]` pairs.

Example:

```yaml
faults:
  FaultTChiBias.k:
    - [0, 0]
    - [3600, 2.0]
```

This means the CHW supply-temperature sensor-bias fault is inactive at simulation start and set to `2.0` after 3600 seconds. See [fault_scenario_configuration.md](docs/fault_scenario_configuration.md) for details.

## Controller Interface

Controllers implement `initialize()` and `compute_setpoint(current_time, step_size)`. The plant expects two control outputs:

- `Tset.k`
- `CHWpumpInput.k`

The built-in RBC baseline is accessed through the `Default_RBC` controller wrapper, which sends zero override values and leaves the FMU embedded RBC logic active. External controllers can partially override these setpoints while the remaining FMU logic continues to operate. See [controller_interface.md](docs/controller_interface.md).

## KPI Evaluation

The platform writes time-series simulation outputs and automatically calculates KPIs including discomfort hours, discomfort degree hours, peak discomfort degree, energy consumption, peak power, energy cost, and calculation time ratio. Fault-tolerant comparison KPIs are documented separately. See [kpi_definitions.md](docs/kpi_definitions.md).

Fault-tolerant control (FTC) KPI comparison is computed from one fault-free result CSV and one faulty result CSV:

```bash
python examples/compare_ftc_kpi.py \
  --baseline-csv results/Default_RBC_results_<fault_free_timestamp>.csv \
  --faulty-csv results/Default_RBC_results_<faulty_timestamp>.csv \
  --name Default_RBC_FTC
```

The FTC comparison reports absolute and relative degradation of generic KPIs plus supply-air temperature and power deviations.

## Relation to BOPTEST

CHWPlantFullTest follows similar benchmarking principles to BOPTEST: a plant emulator, a controller-facing interface, scenario definition, and KPI evaluation. It is not currently a BOPTEST test case and does not implement the BOPTEST API. A BOPTEST-style adapter is a future extension.

## Testing

Run lightweight tests:

```bash
pytest
```

The FMU smoke test is skipped automatically when PyFMI or the FMU files are unavailable.

## License

This project is released under the MIT License. See the LICENSE file for details.

Third-party models, libraries, weather files, and datasets remain subject to their original licenses. See `THIRD_PARTY_LICENSES.md`.

## Citation

Citation metadata is provided in `CITATION.cff`. The associated manuscript is currently under review and will be added after publication.

## Contact

Contact information is not provided in this release.

