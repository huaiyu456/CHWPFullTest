from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from chwplantfulltest.control.controller_base import ControllerBase


class CustomController(ControllerBase):
    """Minimal external controller template.

    The FMU contains the embedded RBC logic. Returning zeros for both control
    inputs leaves the embedded baseline behavior active in the current model.
    Replace these values to partially override selected setpoints.
    """

    def initialize(self):
        self.tset_k = self.config.get("tset_k", 0.0)
        self.chw_input = self.config.get("chw_input", 0.0)

    def compute_setpoint(self, current_time, step_size):
        return self.tset_k, self.chw_input


if __name__ == "__main__":
    print("CustomController template loaded.")
