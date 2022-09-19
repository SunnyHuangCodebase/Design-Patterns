import pytest

from patterns.behavioral.state.smart_bathtub import BathTubMode, ColdBath, CoolPostExerciseRinse, CoolingMist, HotBath, MassageTherapy, Sauna, SmartBathtub, Toggle, UnusedBath, WarmPostExerciseRinse, WaterPressure, WaterTemperature


class TestState:

  @pytest.fixture
  def smart_tub(self):
    default = UnusedBath()
    return SmartBathtub(default)

  def test_default_tub(self, smart_tub: SmartBathtub):
    assert smart_tub.mode == BathTubMode.OFF
    assert smart_tub.water_temperature == WaterTemperature.COLD
    assert smart_tub.pressure == WaterPressure.OFF
    assert smart_tub.drain == Toggle.OFF
    assert smart_tub.diverter == Toggle.OFF
    assert smart_tub.overflow_pipe == Toggle.OFF

  def test_cold_bath(self, smart_tub: SmartBathtub):
    smart_tub.change_state(ColdBath())
    assert smart_tub.mode == BathTubMode.BATH
    assert smart_tub.water_temperature == WaterTemperature.COLD
    assert smart_tub.pressure == WaterPressure.HIGH
    assert smart_tub.drain == Toggle.OFF
    assert smart_tub.diverter == Toggle.OFF
    assert smart_tub.overflow_pipe == Toggle.ON

  def test_hot_bath(self, smart_tub: SmartBathtub):
    smart_tub.change_state(HotBath())
    assert smart_tub.mode == BathTubMode.BATH
    assert smart_tub.water_temperature == WaterTemperature.HOT
    assert smart_tub.pressure == WaterPressure.HIGH
    assert smart_tub.drain == Toggle.OFF
    assert smart_tub.diverter == Toggle.OFF
    assert smart_tub.overflow_pipe == Toggle.ON

  def test_sauna(self, smart_tub: SmartBathtub):
    smart_tub.change_state(Sauna())
    assert smart_tub.mode == BathTubMode.MIST
    assert smart_tub.water_temperature == WaterTemperature.HOT
    assert smart_tub.pressure == WaterPressure.LOW
    assert smart_tub.drain == Toggle.ON
    assert smart_tub.diverter == Toggle.ON
    assert smart_tub.overflow_pipe == Toggle.OFF

  def test_cooling_mist(self, smart_tub: SmartBathtub):
    smart_tub.change_state(CoolingMist())
    assert smart_tub.mode == BathTubMode.MIST
    assert smart_tub.water_temperature == WaterTemperature.COLD
    assert smart_tub.pressure == WaterPressure.LOW
    assert smart_tub.drain == Toggle.ON
    assert smart_tub.diverter == Toggle.ON
    assert smart_tub.overflow_pipe == Toggle.OFF

  def test_cool_post_exercise_rinse(self, smart_tub: SmartBathtub):
    smart_tub.change_state(CoolPostExerciseRinse())
    assert smart_tub.mode == BathTubMode.SPRAY
    assert smart_tub.water_temperature == WaterTemperature.COOL
    assert smart_tub.pressure == WaterPressure.MED
    assert smart_tub.drain == Toggle.ON
    assert smart_tub.diverter == Toggle.ON
    assert smart_tub.overflow_pipe == Toggle.OFF

  def test_warm_post_exercise_rinse(self, smart_tub: SmartBathtub):
    smart_tub.change_state(WarmPostExerciseRinse())
    assert smart_tub.mode == BathTubMode.SPRAY
    assert smart_tub.water_temperature == WaterTemperature.WARM
    assert smart_tub.pressure == WaterPressure.MED
    assert smart_tub.drain == Toggle.ON
    assert smart_tub.diverter == Toggle.ON
    assert smart_tub.overflow_pipe == Toggle.OFF

  def test_massage_therapy(self, smart_tub: SmartBathtub):
    smart_tub.change_state(MassageTherapy())
    assert smart_tub.mode == BathTubMode.JET
    assert smart_tub.water_temperature == WaterTemperature.WARM
    assert smart_tub.pressure == WaterPressure.HIGH
    assert smart_tub.drain == Toggle.ON
    assert smart_tub.diverter == Toggle.ON
    assert smart_tub.overflow_pipe == Toggle.OFF


if __name__ == "__main__":
  pytest.main([__file__])
