# KPI Definitions

The generic KPI module calculates:

- DH or UH: discomfort or unmet hours above the comfort threshold.
- DDH or UDH: degree-hours above the comfort threshold.
- PUD: peak unmet or discomfort degree.
- CEC: cycle energy consumption.
- PEC: peak energy consumption.
- CECC: cycle energy consumption cost.
- CTR: calculation time ratio.

## FTC KPI

Fault-tolerant control (FTC) KPIs are calculated by comparing faulty-condition KPIs with a fault-free baseline:

- Absolute degradation: `KPI_faulty - KPI_fault_free`.
- Relative degradation percentage: `(KPI_faulty - KPI_fault_free) / KPI_fault_free * 100`.

The implementation is available in `chwplantfulltest/kpi/ftc_kpi.py`.

Run a comparison after generating one fault-free result CSV and one faulty-condition result CSV:

```bash
python examples/compare_ftc_kpi.py \
  --baseline-csv results/Default_RBC_results_<fault_free_timestamp>.csv \
  --faulty-csv results/Default_RBC_results_<faulty_timestamp>.csv \
  --name Default_RBC_FTC
```

The FTC output includes:

- Generic KPI absolute degradation.
- Generic KPI relative degradation ratio.
- Mean supply-air temperature deviation.
- Maximum absolute supply-air temperature deviation.
- Mean power deviation.
- Maximum absolute power deviation.

Outputs are saved to `results/` by default:

- `<Controller>_results_<timestamp>.csv`
- `<Controller>_KPI_results_<timestamp>.csv`
- `<Controller>_KPI_results_<timestamp>.txt`

The code is available in `chwplantfulltest/kpi/` and exposed through `chwplantfulltest/metrics.py`.

