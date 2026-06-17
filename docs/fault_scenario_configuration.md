# Fault Scenario Configuration

Example test settings are defined by YAML files in `configs/`.

- `examples/run_fault_free_rbc.py` loads `configs/fault_free.yaml`.
- `examples/run_sensor_bias_rbc.py` loads `configs/sensor_bias.yaml`.
- `examples/run_pump_stuck_rbc.py` loads `configs/pump_stuck.yaml`.

The package runner can also load any compatible YAML scenario:

```bash
PYTHONPATH=src python -m chwplantfulltest.runner --config configs/sensor_bias.yaml
```

## Common Fields

```yaml
name: sensor_bias_tchi
description: Built-in RBC baseline with CHW supply-temperature sensor bias.
controller: Default_RBC
mode: test
start_time: 0
step_size: 600
num_steps: 12
results_dir: results
faults:
  FaultTChiBias.k:
    - [0, 0]
    - [3600, 2.0]
```

- `start_time`: FMU simulation start time in seconds.
- `step_size`: control and simulation step size in seconds.
- `num_steps`: total number of simulation steps.
- `results_dir`: directory used for output CSV and KPI files.
- `faults`: dictionary whose keys are FMU fault parameters and whose values are time schedules.

Each fault schedule is a list of `[fault_start_time, value]` entries. The value remains active until a later entry changes it. Fault duration is therefore defined by the interval between `fault_start_time` and the next scheduled time. If there is no later time, the fault remains active until the end of the simulation.

## Supported Fault Parameters

- `FaultTChiBias.k`
- `FaultTWSEBias.k`
- `FaultTairBias.k`
- `FaultCHWPumpStuck.k`
- `FaultCHWPumpLeak.k`
- `FaultWSEValveStuck.k`
- `FaultWSEValveLeak.k`
- `FaultChiValveStuck.k`
- `FaultChiValveLeak.k`
- `FaultPipeLeak.k`

## Examples

Fault-free operation:

```yaml
faults: {}
```

CHW supply-temperature sensor bias:

```yaml
faults:
  FaultTChiBias.k:
    - [0, 0]
    - [3600, 2.0]
```

CHW pump-stuck fault:

```yaml
faults:
  FaultCHWPumpStuck.k:
    - [0, 0]
    - [3600, 30000]
```

Multiple faults can be configured by adding multiple keys under `faults`.
