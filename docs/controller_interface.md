# Controller Interface

Controllers derive from `chwplantfulltest.control.controller_base.ControllerBase`.

Required methods:

- `initialize()`: read configuration and initialize controller state.
- `compute_setpoint(current_time, step_size)`: return the control values for the next FMU step.

Expected outputs:

- `Tset.k`: chilled water temperature setpoint override signal.
- `CHWpumpInput.k`: chilled water pump input override signal.

Available inputs are read from the FMU through `self.model.get(...)`. Common signals include:

- `TAirSup.T`
- `weaBus.TWetBul`
- `weaBus.TDryBul`
- `PAllAgg.y`
- `PAllAgg.y`

The built-in RBC baseline differs from external controllers because the core RBC logic is embedded in the FMU. The `Default_RBC` controller returns zero values for the override channels, which leaves the embedded RBC active. Future external controllers may partially override selected setpoints through the same interface.

External controllers can be loaded by module and class name:

```bash
PYTHONPATH=src python -m chwplantfulltest.runner \
  --config configs/fault_free.yaml \
  --controller-module sample_controller \
  --controller-class SampleController \
  --controller-path user_controllers
```

The same fields can be placed in a YAML scenario:

```yaml
controller_path: user_controllers
controller_module: sample_controller
controller_class: SampleController
controller_params:
  tset_k: 0
  chw_input: 0
```

See `examples/custom_controller_template.py` for a minimal template.

