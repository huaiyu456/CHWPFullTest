from .controller_base import ControllerBase


class DefaultRBCController(ControllerBase):
    DEFAULT_CONFIG = {
        "temp_param": {"name": "Tset.k", "default_value_k": 0},
        "chw_param": {"name": "CHWpumpInput.k", "default_value": 0},
    }

    def initialize(self):
        temp_cfg = self.config["temp_param"]
        self.temp_name = temp_cfg["name"]
        self.default_temp = temp_cfg["default_value_k"]
        chw_cfg = self.config["chw_param"]
        self.chw_name = chw_cfg["name"]
        self.default_chw = chw_cfg["default_value"]

    def compute_setpoint(self, current_time, step_size):
        return self.default_temp, self.default_chw
