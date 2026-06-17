from pathlib import Path

import yaml

from chwplantfulltest.config import PlatformConfig


def test_example_yaml_configs_load():
    root = Path(__file__).resolve().parents[1]
    for name in ["fault_free.yaml", "sensor_bias.yaml", "pump_stuck.yaml"]:
        data = yaml.safe_load((root / "configs" / name).read_text(encoding="utf-8"))
        assert "name" in data
        assert "controller" in data
        assert "faults" in data


def test_platform_config_defaults_are_relative_to_repo():
    cfg = PlatformConfig(num_steps=1)
    cfg.resolve_paths()
    assert cfg.model_path.endswith("models\\DataCenterCHWP_HybridFault.fmu") or cfg.model_path.endswith("models/DataCenterCHWP_HybridFault.fmu")
    assert cfg.results_dir.endswith("results")

