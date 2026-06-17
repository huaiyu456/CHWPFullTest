# Installation

Recommended environment:

```bash
conda create -n chwplantfulltest python=3.10
conda activate chwplantfulltest
conda install -c conda-forge pyfmi
pip install -r requirements.txt
```

PyFMI can be difficult to install with plain `pip` because it depends on FMI and numerical runtime libraries. Use conda-forge for local simulation runs.

The public RBC platform does not require TensorFlow or SciPy.

