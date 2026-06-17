def test_import_chwplantfulltest():
    import chwplantfulltest

    assert chwplantfulltest is not None


def test_import_controller_base():
    from chwplantfulltest.control.controller_base import ControllerBase

    assert hasattr(ControllerBase, "compute_setpoint")

