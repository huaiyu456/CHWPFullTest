import os
import pickle
import shutil

import numpy as np


class FMUStateManager:
    def __init__(self, model, state_dir="saved_states"):
        self.model = model
        self.state_dir = state_dir
        self._initialize_directory()

    def _initialize_directory(self):
        if os.path.exists(self.state_dir):
            shutil.rmtree(self.state_dir)
        os.makedirs(self.state_dir, exist_ok=True)

    def get_in_memory_state(self):
        try:
            return self.model.get_fmu_state()
        except Exception:
            return None

    def restore_in_memory_state(self, fmu_state, free_memory=True):
        if fmu_state is None:
            return False
        try:
            self.model.set_fmu_state(fmu_state)
            if free_memory:
                self.model.free_fmu_state(fmu_state)
            return True
        except Exception:
            return False



