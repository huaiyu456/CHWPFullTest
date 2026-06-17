from pathlib import Path

import pytest


def test_optional_fmu_smoke_prerequisites():
    pytest.importorskip("pyfmi")
    root = Path(__file__).resolve().parents[1]
    fmu_path = root / "models" / "DataCenterCHWP_HybridFault.fmu"
    if not fmu_path.exists():
        pytest.skip("FMU file is not available.")
    assert fmu_path.exists()

