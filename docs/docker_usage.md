# Docker Usage

Docker is the second supported execution mode. Local execution is intended for development and debugging; Docker execution is intended for reproducible deployment.

## Prerequisites

- Docker Engine or Docker Desktop.
- The FMU must include a Linux binary: `binaries/linux64/*.so`.
- The FMU weather path must be relative to the project root, for example `weather/CHN_Guangdong.Shenzhen.594930_SWERA.mos`.

## Build

From the repository root:

```bash
docker compose build
```

## Run Default Scenarios

Short smoke test:

```bash
docker compose run --rm chwplantfulltest --config configs/smoke_test.yaml
```

Fault-free baseline:

```bash
docker compose run --rm chwplantfulltest --config configs/fault_free.yaml
```

Sensor-bias fault:

```bash
docker compose run --rm chwplantfulltest --config configs/sensor_bias.yaml
```

Pump-stuck fault:

```bash
docker compose run --rm chwplantfulltest --config configs/pump_stuck.yaml
```

Result CSV and KPI files are written to `results/` on the host machine.

## Custom Scenario

Create or edit a YAML file under `configs/`:

```yaml
name: my_fault
controller: Default_RBC
mode: test
start_time: 0
step_size: 600
num_steps: 144
results_dir: results
faults:
  FaultTChiBias.k:
    - [0, 0]
    - [3600, 2.0]
```

Run it:

```bash
docker compose run --rm chwplantfulltest --config configs/my_fault.yaml
```

## User Controller

Place a controller file under `user_controllers/`, for example `user_controllers/my_controller.py`:

```python
from chwplantfulltest.control.controller_base import ControllerBase


class MyController(ControllerBase):
    def initialize(self):
        self.tset_k = self.config.get("tset_k", 0.0)
        self.chw_input = self.config.get("chw_input", 0.0)

    def compute_setpoint(self, current_time, step_size):
        return self.tset_k, self.chw_input
```

Run it with command-line overrides:

```bash
docker compose run --rm chwplantfulltest \
  --config configs/fault_free.yaml \
  --controller-module my_controller \
  --controller-class MyController \
  --controller-path user_controllers
```

Or define it in YAML:

```yaml
controller_path: user_controllers
controller_module: my_controller
controller_class: MyController
controller_params:
  tset_k: 0
  chw_input: 0
```

Then run:

```bash
docker compose run --rm chwplantfulltest --config configs/custom_controller.yaml
```

## FTC KPI In Docker

The runner entrypoint is configured for simulation. To run FTC KPI comparison, override the entrypoint:

```bash
docker compose run --rm --entrypoint conda chwplantfulltest \
  run --no-capture-output -n base python examples/compare_ftc_kpi.py \
  --baseline-csv results/Default_RBC_results_<fault_free_timestamp>.csv \
  --faulty-csv results/Default_RBC_results_<faulty_timestamp>.csv \
  --name Default_RBC_FTC
```
