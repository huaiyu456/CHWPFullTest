from chwplantfulltest.control.controller_base import ControllerBase


class SampleController(ControllerBase):
    """Example user controller for Docker and local extension tests."""

    def initialize(self):
        self.tset_k = self.config.get("tset_k", 0.0)
        self.chw_input = self.config.get("chw_input", 0.0)

    def compute_setpoint(self, current_time, step_size):
        return self.tset_k, self.chw_input
