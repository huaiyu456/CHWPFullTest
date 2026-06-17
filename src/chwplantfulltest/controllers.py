from dataclasses import dataclass
import importlib
import sys
from pathlib import Path
from typing import Any, Dict


CONTROLLER_REGISTRY = {
    "Default_RBC": "chwplantfulltest.control.default_rbc_controller:DefaultRBCController",
}


@dataclass
class ControllerSpec:
    controller_type: str
    params: Dict[str, Any]


def create_controller(controller_type, *args, **kwargs):
    if controller_type not in CONTROLLER_REGISTRY:
        raise ValueError(f"Unknown controller: {controller_type}")
    module_name, class_name = CONTROLLER_REGISTRY[controller_type].split(":")
    module = importlib.import_module(module_name)
    controller_cls = getattr(module, class_name)
    return controller_cls(*args, **kwargs)


def create_external_controller(module_name, class_name, *args, controller_path=None, **kwargs):
    if controller_path:
        path = str(Path(controller_path).resolve())
        if path not in sys.path:
            sys.path.insert(0, path)
    module = importlib.import_module(module_name)
    controller_cls = getattr(module, class_name)
    return controller_cls(*args, **kwargs)
