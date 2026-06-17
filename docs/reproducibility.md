# Reproducibility Checklist

- Software version: record the Git commit hash after publishing.
- Python version: Python 3.10 recommended.
- Dependencies: install from `requirements.txt`; use conda-forge for PyFMI.
- FMU/model file: `models/DataCenterCHWP_HybridFault.fmu`.
- Weather file: `weather/CHN_Guangdong.Shenzhen.594930_SWERA.mos`.
- Configuration files: `configs/`.
- Random seed: not required for the deterministic built-in RBC examples.
- Default example command: `python examples/run_fault_free_rbc.py`.
- Output location: `results/`.
- Smoke tests: run `pytest`.
- Docker support is provided for reproducible deployment when the FMU includes `binaries/linux64/*.so`.
- External research controllers are not included in this public upload, but users can mount or add their own controllers through `user_controllers/`.

