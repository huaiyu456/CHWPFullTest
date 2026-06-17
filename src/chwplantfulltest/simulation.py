import csv
import os
import time
from datetime import datetime

from pyfmi import load_fmu

from chwplantfulltest.utils.state_manager import FMUStateManager
from chwplantfulltest.controllers import create_controller, create_external_controller


class PlatformSimulation:
    def __init__(self, config):
        self.config = config
        self.config.validate()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        self.controller_type = config.controller_type
        self.config.resolve_paths()
        self.results_dir = self.config.results_dir
        os.makedirs(self.results_dir, exist_ok=True)
        self.csv_filename = os.path.join(self.results_dir, f"{self.controller_type}_results_{self.timestamp}.csv")
        self.results = self._init_results_dict()
        self.initialize_csv()

    def _init_results_dict(self):
        return {
            "time": [], "Tset": [], "PAllAgg": [], "reward": [], "computation_time": [], "delta_power": [],
            "fault_param_values": {k: {} for k in self.config.fault_param_changes.keys()},
        }

    def initialize_csv(self):
        headers = [
            "Step", "StartTime", "EndTime", "ComputationTime", "Reward", "TAirSup.T", "chi.TSet",
            "con.TSet", "chi.on", "CHWpumpInput.k", "PAll1.y", "EnergyAgg.y", "SCOP.y",
            "chi.QCon_flow", "wse.Q1_flow", "PChi1.y", "PCooTowFan1.y", "PSupFan1.y",
            "PChiWatPum1.y", "PConWatPum1.y", "PWSEWatPum1.y", "PCTWatPum.y",
            "pumCHW.m_flow", "val1.m_flow", "valByp.m_flow", "weaBus.TWetBul", "weaBus.TDryBul"
        ]
        with open(self.csv_filename, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(headers)

    def initialize(self):
        # The FMU resolves relative resources such as weather/*.mos from the process cwd.
        os.chdir(self.config.project_root)
        self.model = load_fmu(self.config.model_path)
        if self.config.weather_file_name and os.path.exists(self.config.weather_file_name):
            try:
                self.model.set("weaData.filNam", self.config.weather_file_name)
            except Exception:
                print("[CHWPlantFullTest] Weather file is defined inside the FMU; external override was ignored.")

        self.state_manager = FMUStateManager(self.model, self.config.state_dir)

        if self.config.controller_module and self.config.controller_class:
            self.controller = create_external_controller(
                self.config.controller_module,
                self.config.controller_class,
                self.model,
                self.state_manager,
                self.config.controller_params,
                controller_path=self.config.controller_path,
            )
        elif self.controller_type == "Default_RBC":
            self.controller = create_controller("Default_RBC", self.model, self.state_manager, self.config.controller_params)
        else:
            raise ValueError(f"Unknown controller: {self.controller_type}")

        self.controller.initialize()
        self.model.setup_experiment(start_time=self.config.start_time)
        self.model.initialize()
        self.current_fault_params = {k: 0.0 for k in self.config.fault_param_changes.keys()}
        self._apply_faults(self.config.start_time)
        self._print_runtime_header()

    def _print_runtime_header(self):
        print(f"[CHWPlantFullTest] Controller: {self.controller_type}")
        if self.config.controller_module and self.config.controller_class:
            print(f"[CHWPlantFullTest] Controller class: {self.config.controller_module}.{self.config.controller_class}")
        print(f"[CHWPlantFullTest] Model: {self.config.model_path}")
        print(f"[CHWPlantFullTest] Working dir: {os.getcwd()}")
        print(f"[CHWPlantFullTest] Results dir: {self.results_dir}")
        print("[CHWPlantFullTest] Fault schedule:")
        for name, plan in self.config.fault_param_changes.items():
            print(f"  - {name}: {plan}")

    def _apply_faults(self, current_time):
        for param, plan in self.config.fault_param_changes.items():
            value = sorted(plan, key=lambda x: x[0])[0][1]
            for time_point, val in sorted(plan, key=lambda x: x[0]):
                if current_time >= time_point:
                    value = val
                else:
                    break
            if abs(self.current_fault_params[param] - value) > 1e-4:
                self.model.set(param, value)
                self.current_fault_params[param] = value
            self.results["fault_param_values"][param][current_time] = value

    def run(self):
        current_time = self.config.start_time
        for step in range(self.config.num_steps):
            self._apply_faults(current_time)
            start_comp = time.time()
            optimal_temp, optimal_chw = self.controller.compute_setpoint(current_time, self.config.step_size)
            comp_time = time.time() - start_comp
            reward = getattr(self.controller, "last_reward", None)
            self.model.set("Tset.k", optimal_temp)
            self.model.set("CHWpumpInput.k", optimal_chw)
            self.model.do_step(current_t=current_time, step_size=self.config.step_size, new_step=True)
            current_time += self.config.step_size
            self._record_results(current_time, optimal_temp, optimal_chw, comp_time, reward)
            self._print_step(step, current_time, optimal_temp, optimal_chw, comp_time, reward)

        if hasattr(self.controller, "finalize"):
            self.controller.finalize(self.timestamp)
        return self.results

    def _print_step(self, step, current_time, optimal_temp, optimal_chw, comp_time, reward):
        try:
            p_all = self.model.get("PAllAgg.y")[0]
            t_air = self.model.get("TAirSup.T")[0] - 273.15
            scop = self.model.get("SCOP.y")[0]
        except Exception:
            p_all, t_air, scop = float("nan"), float("nan"), float("nan")
        reward_text = "NA" if reward is None else f"{reward:.3f}"
        print(
            f"[CHWPlantFullTest][{self.controller_type}] step {step + 1}/{self.config.num_steps} "
            f"t={current_time:.0f}s Tset={optimal_temp - 273.15:.2f}C "
            f"CHW={optimal_chw:.0f} P={p_all:.2f}W Tair={t_air:.2f}C SCOP={scop:.3f} reward={reward_text} "
            f"comp={comp_time:.3f}s"
        )

    def _record_results(self, current_time, optimal_temp, optimal_chw, comp_time, reward):
        self.results["time"].append(current_time)
        self.results["Tset"].append(optimal_temp - 273.15)
        self.results["PAllAgg"].append(self.model.get("PAllAgg.y")[0])
        self.results["reward"].append(reward)
        self.results["computation_time"].append(comp_time)
        delta = self.results["PAllAgg"][-1] - self.results["PAllAgg"][-2] if len(self.results["PAllAgg"]) > 1 else 0
        self.results["delta_power"].append(delta)
        self.record_step_to_csv(
            len(self.results["time"]),
            current_time - self.config.step_size,
            current_time,
            comp_time,
            reward,
        )

    def record_step_to_csv(self, step, start_time, end_time, comp_time, reward):
        row_data = [
            step, start_time, end_time, comp_time, reward,
            self.model.get("TAirSup.T")[0], self.model.get("chi.TSet")[0], self.model.get("add1.u2")[0],
            self.model.get("chi.on")[0], self.model.get("CHWpumpdpInput.y")[0], self.model.get("PAll1.y")[0],
            self.model.get("gain.y")[0], self.model.get("SCOP.y")[0], self.model.get("chi.QCon_flow")[0],
            self.model.get("wse.Q1_flow")[0], self.model.get("PChi1.y")[0], self.model.get("PCooTowFan1.y")[0],
            self.model.get("PSupFan1.y")[0], self.model.get("PChiWatPum1.y")[0], self.model.get("PConWatPum1.y")[0],
            self.model.get("PWSEWatPum1.y")[0], self.model.get("PCTWatPum.y")[0], self.model.get("pumCHW.m_flow")[0],
            self.model.get("val1.m_flow")[0], self.model.get("valByp.m_flow")[0],
            self.model.get("weaBus.TWetBul")[0], self.model.get("weaBus.TDryBul")[0]
        ]
        with open(self.csv_filename, "a", newline="", encoding="utf-8") as csvfile:
            csv.writer(csvfile).writerow(row_data)


