from dataclasses import dataclass, field
import os
from typing import Dict, List, Tuple, Any


FaultPlan = List[Tuple[float, float]]


@dataclass
class PlatformConfig:
    model_path: str = "models/DataCenterCHWP_HybridFault.fmu"
    start_time: float = 0.0
    step_size: float = 600.0
    num_steps: int = 6 * 24 * 7
    results_dir: str = "results"
    state_dir: str = os.path.join("runtime", "saved_states")
    weather_file_name: str | None = None
    controller_type: str = "Default_RBC"
    controller_mode: str = "test"
    project_root: str = ""
    controller_module: str | None = None
    controller_class: str | None = None
    controller_path: str | None = None
    controller_params: Dict[str, Any] = field(default_factory=dict)
    fault_param_changes: Dict[str, FaultPlan] = field(default_factory=dict)

    def validate(self) -> None:
        if self.step_size <= 0:
            raise ValueError("step_size must be positive")
        if self.num_steps <= 0:
            raise ValueError("num_steps must be positive")
        if self.controller_type != "Default_RBC" and not (self.controller_module and self.controller_class):
            raise ValueError(f"Unsupported controller_type: {self.controller_type}")
        if self.controller_mode not in {"train", "test"}:
            raise ValueError(f"Unsupported controller_mode: {self.controller_mode}")
        for param, plan in self.fault_param_changes.items():
            if not plan:
                raise ValueError(f"Fault plan for {param} cannot be empty")
            last_t = None
            for t, _ in plan:
                if last_t is not None and t < last_t:
                    raise ValueError(f"Fault plan for {param} must be time-sorted")
                last_t = t

    def resolve_paths(self) -> None:
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.project_root = root_dir
        self.model_path = os.path.abspath(os.path.join(root_dir, self.model_path))
        self.results_dir = os.path.abspath(os.path.join(root_dir, self.results_dir))
        self.state_dir = os.path.abspath(os.path.join(root_dir, self.state_dir))
        if self.controller_path:
            self.controller_path = os.path.abspath(os.path.join(root_dir, self.controller_path))

