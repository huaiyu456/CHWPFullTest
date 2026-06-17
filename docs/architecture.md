# Architecture

CHWPlantFullTest is a Python-FMU test platform for reproducible chilled water plant controller benchmarking.

The four major modules are:

- CHWP Model Module: FMU files and weather data used by the plant emulator.
- Scenario Setting Module: fault-free and faulty scenario definitions.
- Control Strategy Module: built-in RBC wrapper and standardized interface for future external controllers.
- Evaluation and Metrics Module: output writing and automated KPI calculation.

The built-in RBC is the default embedded baseline controller. In the current FMU, setting override inputs to zero leaves the embedded rule-based logic active. This behavior is wrapped by `DefaultRBCController`.

External controllers can be integrated later by implementing the controller interface in `src/chwplantfulltest/control/controller_base.py`. They may partially override `Tset.k` and `CHWpumpInput.k` while the remaining embedded plant logic continues to run.

Research controllers are intentionally excluded from this public upload. They can be added later through the documented controller interface if needed.

## Relation to BOPTEST

CHWPlantFullTest follows BOPTEST-style benchmarking principles: plant emulation, a controller interface, scenario definition, and KPI evaluation. It is not currently a BOPTEST test case and does not provide a BOPTEST API. API alignment can be added as future work.

