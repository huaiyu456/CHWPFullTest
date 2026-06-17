from chwplantfulltest.kpi.ftc_kpi import calculate_ftc_kpi


def test_ftc_kpi_on_synthetic_data():
    baseline_kpi = {
        "Discomfort hours (DH)": "1.00 h",
        "Cycle Energy Consumption": "10.00 kWh",
    }
    faulty_kpi = {
        "Discomfort hours (DH)": "1.50 h",
        "Cycle Energy Consumption": "12.00 kWh",
    }
    baseline_csv = [
        {"TAirSup.T": 300.15, "PAll1.y": 10000.0},
        {"TAirSup.T": 300.15, "PAll1.y": 11000.0},
    ]
    faulty_csv = [
        {"TAirSup.T": 301.15, "PAll1.y": 12000.0},
        {"TAirSup.T": 302.15, "PAll1.y": 13000.0},
    ]
    kpi = calculate_ftc_kpi(baseline_kpi, faulty_kpi, baseline_csv, faulty_csv)
    assert kpi["Discomfort hours (DH) degradation"] == "0.5"
    assert kpi["Cycle Energy Consumption degradation ratio"] == "20.00 %"
    assert "Mean supply-air temperature deviation" in kpi
