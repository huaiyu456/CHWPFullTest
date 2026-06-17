from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

from chwplantfulltest.config import PlatformConfig


FaultPlan = List[Tuple[float, float]]


@dataclass
class FaultScenario:
    name: str
    fault_param_changes: Dict[str, FaultPlan] = field(default_factory=dict)


def default_no_fault() -> FaultScenario:
    return FaultScenario(
        name="NoFault",
        fault_param_changes={
            "FaultTChiBias.k": [(0, 0)],
            "FaultTWSEBias.k": [(0, 0)],
            "FaultTairBias.k": [(0, 0)],
            "FaultCHWPumpStuck.k": [(0, 0)],
            "FaultCHWPumpLeak.k": [(0, 0)],
            "FaultWSEValveStuck.k": [(0, 0)],
            "FaultWSEValveLeak.k": [(0, 0)],
            "FaultChiValveStuck.k": [(0, 0)],
            "FaultChiValveLeak.k": [(0, 0)],
            "FaultPipeLeak.k": [(0, 0)],
        },
    )


def load_platform_config(config_path: str | Path) -> PlatformConfig:
    path = Path(config_path)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    faults = {
        name: [(float(t), float(value)) for t, value in schedule]
        for name, schedule in (data.get("faults") or {}).items()
    }

    return PlatformConfig(
        start_time=float(data.get("start_time", 0.0)),
        step_size=float(data.get("step_size", 600.0)),
        num_steps=int(data.get("num_steps", 12)),
        results_dir=data.get("results_dir", "results"),
        controller_type=data.get("controller", "Default_RBC"),
        controller_mode=data.get("mode", "test"),
        controller_module=data.get("controller_module"),
        controller_class=data.get("controller_class"),
        controller_path=data.get("controller_path"),
        controller_params=data.get("controller_params") or {},
        fault_param_changes=faults,
    )
