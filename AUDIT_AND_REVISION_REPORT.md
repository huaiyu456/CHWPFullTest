# Audit and Revision Report

Date: 2026-06-15

## Scope

This report covers the standalone public GitHub project in this `github/` directory. Internal development folders outside this directory are not required for the public release.

## Standalone Repository Structure

- `src/chwplantfulltest/`: installable Python package.
- `models/DataCenterCHWP_HybridFault.fmu`: FMU file used by the examples.
- `weather/CHN_Guangdong.Shenzhen.594930_SWERA.mos`: weather file included with the public upload.
- `configs/`: example scenario configuration files.
- `examples/`: runnable scripts from the repository root.
- `docs/`: installation, architecture, controller interface, fault scenario, KPI, and reproducibility documentation.
- `tests/`: lightweight pytest tests.
- `results/`: default output directory, tracked only with `.gitkeep`.

## Implementation Notes

- The public package no longer depends on external internal-development folders.
- Default FMU paths resolve to `models/`.
- The default FMU is `models/DataCenterCHWP_HybridFault.fmu`.
- Default outputs resolve to `results/`.
- The built-in RBC is documented as the minimum runnable baseline.
- External research controller files were removed from the public upload.
- The public upload does not require TensorFlow or SciPy.
- Generated logs, runtime state folders, cached bytecode, and example outputs are excluded from upload.

## License and Attribution

The project contains a root-level MIT License. Third-party models, FMUs, weather files, libraries, and datasets are not relicensed. Attribution and redistribution cautions are documented in `THIRD_PARTY_LICENSES.md`.

## Verification Status

Verification performed on the cleaned public upload confirmed:

- Python compile check passed for modified platform files, examples, and tests.
- Built-in RBC fault-free example ran successfully.
- Built-in RBC sensor-bias example ran successfully.
- Built-in RBC pump-stuck example ran successfully.
- Project scan found no references to removed research controllers or their dependencies.

To reproduce verification from the repository root, run:

```bash
python -m py_compile src/chwplantfulltest/config.py src/chwplantfulltest/simulation.py
python examples/run_fault_free_rbc.py
python examples/run_sensor_bias_rbc.py
python examples/run_pump_stuck_rbc.py
python -m pytest -q
```

`pytest` must be installed in the active Python environment. The FMU smoke test skips if PyFMI or the FMU files are unavailable.

## Remaining Items Before Public Release

- Author and institution metadata have been added. Repository URL and manuscript citation should be updated after the public repository is created and the associated manuscript is published.
- Verify redistribution rights for all FMU and weather files in `models/` and `weather/`.
- Confirm PyFMI installation instructions on the target operating systems.

## Step 2 Docker Preparation

Docker support has been added as the second execution mode. It includes a conda-forge based PyFMI runtime, result/runtime volume mapping, scenario configuration support, user controller mounting through `user_controllers/`, and Docker usage documentation.
