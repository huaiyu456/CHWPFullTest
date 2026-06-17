class ControllerBase:
    DEFAULT_CONFIG = {}

    def __init__(self, model, state_manager, config=None):
        self.model = model
        self.state_manager = state_manager
        self.config = {**self.DEFAULT_CONFIG, **(config or {})}

    def initialize(self):
        pass

    def compute_setpoint(self, current_time, step_size):
        raise NotImplementedError

    def apply_external_changes(self, current_time):
        pass

    def finalize(self, timestamp=None):
        pass

    def get_results(self):
        return {}



