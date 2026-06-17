from chwplantfulltest.kpi.generic_kpi import calculate_generic_kpi


def test_generic_kpi_on_synthetic_data():
    results = {
        "time": [0, 600, 1200],
        "computation_time": [0.1, 0.1, 0.1],
    }
    csv_data = [
        {"EndTime": 0, "TAirSup.T": 299.15, "EnergyAgg.y": 0.0, "PAll1.y": 10000.0},
        {"EndTime": 600, "TAirSup.T": 300.65, "EnergyAgg.y": 1.0, "PAll1.y": 12000.0},
        {"EndTime": 1200, "TAirSup.T": 301.15, "EnergyAgg.y": 2.0, "PAll1.y": 11000.0},
    ]
    kpi = calculate_generic_kpi(results, csv_data)
    assert "Discomfort hours (DH)" in kpi
    assert "Cycle Energy Consumption" in kpi
    assert "Calculation time ratio" in kpi

