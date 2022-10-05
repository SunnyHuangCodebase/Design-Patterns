"""The Smart Bathtub implements the State design pattern.

Each bathtub mode subclasses an abstract base class called BathtubState.
Alternatively, BathtubState can also be defined as a protocol.

The tub's default state is Off and comes with several modes (states).

When the tub receives updates, it may be desirable to add new modes.
Doing so simply requires creating a new subclass of BathtubState.
If BathtubState is a protocol, create a new class that follows the protocol.

Since no modifications are made to SmartBathtub for new features,
the State pattern abides by the Open-Closed Principle of SOLID, in that
objects should be open to extension but closed to modification.

The State design pattern focuses on how an object's state changes its behavior.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto


class BathTubMode(Enum):
  """Bathtub mode."""
  BATH = auto()
  MIST = auto()
  SPRAY = auto()
  JET = auto()
  WATERFALL = auto()
  OFF = auto()


class WaterPressure(Enum):
  """Shower head spray intensity."""
  OFF = auto()
  LOW = auto()
  MED = auto()
  HIGH = auto()


class WaterTemperature(int, Enum):
  """Water temperature in Fahrenheit."""
  HOT = 105
  WARM = 95
  COOL = 85
  COLD = 75


class Toggle(Enum):
  ON = auto()
  OFF = auto()


class BathTubState(ABC):
  """The interface of a bathtub's state."""
  tub: SmartBathtub

  @abstractmethod
  def adjust_bathtub(self):
    """Controls bathtub."""


class Off(BathTubState):
  """Turns off all features of the tub."""

  def adjust_bathtub(self):
    self.tub.adjust_bathtub_mode(BathTubMode.OFF)
    self.tub.adjust_water_temperature(WaterTemperature.COLD)
    self.tub.adjust_water_pressure(WaterPressure.OFF)
    self.tub.toggle_drain(Toggle.OFF)
    self.tub.toggle_diverter(Toggle.OFF)
    self.tub.toggle_overflow_pipe(Toggle.OFF)


class SmartBathtub:
  """Smart bathtub composed of a state class which controls other attributes."""
  _state: BathTubState
  water_temperature: WaterTemperature
  pressure: WaterPressure
  mode: BathTubMode
  drain: Toggle
  diverter: Toggle
  overflow_pipe: Toggle

  def __init__(self, state: BathTubState):
    self.change_state(state)

  def change_state(self, state: BathTubState):
    self._state = state
    self._state.tub = self
    self._state.adjust_bathtub()

  def adjust_water_temperature(self, temperature: WaterTemperature):
    self.water_temperature = temperature

  def adjust_water_pressure(self, pressure: WaterPressure):
    self.pressure = pressure

  def adjust_bathtub_mode(self, mode: BathTubMode):
    self.mode = mode

  def toggle_drain(self, toggle: Toggle):
    self.drain = toggle

  def toggle_diverter(self, toggle: Toggle):
    self.diverter = toggle

  def toggle_overflow_pipe(self, toggle: Toggle):
    self.overflow_pipe = toggle


class ColdBath(BathTubState):
  """Fills the tub with cold water."""

  def adjust_bathtub(self):
    self.tub.adjust_bathtub_mode(BathTubMode.BATH)
    self.tub.adjust_water_temperature(WaterTemperature.COLD)
    self.tub.adjust_water_pressure(WaterPressure.HIGH)
    self.tub.toggle_drain(Toggle.OFF)
    self.tub.toggle_diverter(Toggle.OFF)
    self.tub.toggle_overflow_pipe(Toggle.ON)


class HotBath(BathTubState):
  """Fills the tub with hot water."""

  def adjust_bathtub(self):
    self.tub.adjust_bathtub_mode(BathTubMode.BATH)
    self.tub.adjust_water_temperature(WaterTemperature.HOT)
    self.tub.adjust_water_pressure(WaterPressure.HIGH)
    self.tub.toggle_drain(Toggle.OFF)
    self.tub.toggle_diverter(Toggle.OFF)
    self.tub.toggle_overflow_pipe(Toggle.ON)


class Sauna(BathTubState):
  """Sprays hot water mist to humidify the tub."""

  def adjust_bathtub(self):
    self.tub.adjust_bathtub_mode(BathTubMode.MIST)
    self.tub.adjust_water_temperature(WaterTemperature.HOT)
    self.tub.adjust_water_pressure(WaterPressure.LOW)
    self.tub.toggle_drain(Toggle.ON)
    self.tub.toggle_diverter(Toggle.ON)
    self.tub.toggle_overflow_pipe(Toggle.OFF)


class CoolingMist(BathTubState):
  """Sprays a cold mist to cool the user while conserving water."""

  def adjust_bathtub(self):
    self.tub.adjust_bathtub_mode(BathTubMode.MIST)
    self.tub.adjust_water_temperature(WaterTemperature.COLD)
    self.tub.adjust_water_pressure(WaterPressure.LOW)
    self.tub.toggle_drain(Toggle.ON)
    self.tub.toggle_diverter(Toggle.ON)
    self.tub.toggle_overflow_pipe(Toggle.OFF)


class CoolPostExerciseRinse(BathTubState):
  """Rinses sweat and dirt off with cool water."""

  def adjust_bathtub(self):
    self.tub.adjust_bathtub_mode(BathTubMode.SPRAY)
    self.tub.adjust_water_temperature(WaterTemperature.COOL)
    self.tub.adjust_water_pressure(WaterPressure.MED)
    self.tub.toggle_drain(Toggle.ON)
    self.tub.toggle_diverter(Toggle.ON)
    self.tub.toggle_overflow_pipe(Toggle.OFF)


class WarmPostExerciseRinse(BathTubState):
  """Rinses sweat and dirt off with warm water."""

  def adjust_bathtub(self):
    self.tub.adjust_bathtub_mode(BathTubMode.SPRAY)
    self.tub.adjust_water_temperature(WaterTemperature.WARM)
    self.tub.adjust_water_pressure(WaterPressure.MED)
    self.tub.toggle_drain(Toggle.ON)
    self.tub.toggle_diverter(Toggle.ON)
    self.tub.toggle_overflow_pipe(Toggle.OFF)


class MassageTherapy(BathTubState):
  """Sprays warm water at high pressure."""

  def adjust_bathtub(self):
    self.tub.adjust_bathtub_mode(BathTubMode.JET)
    self.tub.adjust_water_temperature(WaterTemperature.WARM)
    self.tub.adjust_water_pressure(WaterPressure.HIGH)
    self.tub.toggle_drain(Toggle.ON)
    self.tub.toggle_diverter(Toggle.ON)
    self.tub.toggle_overflow_pipe(Toggle.OFF)
