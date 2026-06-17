# Third-Party Licenses and Attributions

This repository is released under the MIT License for the original platform code. Third-party models, libraries, weather files, datasets, and FMU tooling remain subject to their original licenses and terms.

## Modelica and FMU Dependencies

- Modelica Buildings Library: used or referenced by FMU/model development workflows. Users must comply with the original Modelica Buildings Library license.
- FMU/FMI tooling: FMU execution depends on FMI-compatible tooling such as PyFMI and its dependencies. These packages retain their original licenses.
- PyFMI: recommended for loading and simulating FMU files from Python. See the PyFMI project documentation and license.

## Plant Models and Reference Data

- Chilled water plant FMU files in `models/` may include or derive from third-party Modelica models, reference data center plant models, or research model artifacts. These materials are not relicensed by this repository.
- Any LBNL/reference data center chilled water plant model components remain subject to their original attribution and licensing requirements.

## Weather Data

- Weather files in `weather/` may originate from public weather datasets such as SWERA, CSWD, TMY, or EnergyPlus weather-data distributions. Users should verify the source and license before redistribution.

## Python Packages

The Python dependencies listed in `requirements.txt` and `environment.yml` remain subject to their package licenses. Key dependencies include NumPy, PyYAML, pytest, and PyFMI, together with the FMI/runtime libraries installed by conda-forge.

## Redistribution Note

Before publishing the repository publicly, verify that every FMU, weather file, trained model, and generated result file is permitted for redistribution. If redistribution rights are unclear, replace the file with instructions for obtaining or generating it.

