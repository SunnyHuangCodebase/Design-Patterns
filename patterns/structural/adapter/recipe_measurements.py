from typing import Any, Protocol


class Unit:
  name: str
  quantity: int | float

  def __init__(self, quantity: int | float):
    self.quantity = quantity


class Grams(Unit):
  name = "grams"


class Pounds(Unit):
  name = "pounds"


class mL(Unit):
  name = "mL"


class Cups(Unit):
  name = "cups"


class Celsius(Unit):
  name = "Celsius"


class Fahrenheit(Unit):
  name = "Fahrenheit"


class IncorrectUnit(Exception):
  """Invalid unit."""


class Metric:
  """Standardized recipe measurements in metric units. Compatible with metric unit recipes."""

  def weight(self, unit: Unit) -> Grams:
    """Return metric weight in grams, if valid."""
    if not isinstance(unit, Grams):
      raise IncorrectUnit
    return self.metric_weight(unit)

  def volume(self, unit: Unit) -> mL:
    """Return metric volume in mL, if valid."""
    if not isinstance(unit, mL):
      raise IncorrectUnit
    return self.metric_volume(unit)

  def temperature(self, unit: Unit) -> Celsius:
    """Return metric temperature in Celsius, if valid."""
    if not isinstance(unit, Celsius):
      raise IncorrectUnit
    return self.metric_temperature(unit)

  def metric_weight(self, unit: Grams) -> Grams:
    """Metric weight."""
    return unit

  def metric_volume(self, unit: mL) -> mL:
    """Metric volume."""
    return unit

  def metric_temperature(self, unit: Celsius) -> Celsius:
    """Metric temperature."""
    return unit


class Imperial:
  """Standardized recipe measurements in imperial units. Compatible with imperial unit recipes."""

  def weight(self, unit: Unit) -> Pounds:
    """Return imperial temperature in pounds, if valid."""
    if not isinstance(unit, Pounds):
      raise IncorrectUnit
    return self.imperial_weight(unit)

  def volume(self, unit: Unit) -> Cups:
    """Return imperial temperature in cups, if valid."""
    if not isinstance(unit, Cups):
      raise IncorrectUnit
    return self.imperial_volume(unit)

  def temperature(self, unit: Unit) -> Fahrenheit:
    """Return imperial temperature in Fahrenheit, if valid."""
    if not isinstance(unit, Fahrenheit):
      raise IncorrectUnit
    return self.imperial_temperature(unit)

  def imperial_weight(self, unit: Pounds) -> Pounds:
    """Imperial weight."""
    return unit

  def imperial_volume(self, unit: Cups) -> Cups:
    """Imperial volume."""
    return unit

  def imperial_temperature(self, unit: Fahrenheit) -> Fahrenheit:
    """Imperial temperature."""
    return unit


class MeasurementSystem(Protocol):
  """Standardized recipe measurement protocols."""

  def weight(self, unit: Unit) -> Any:
    """Mass of an ingredient."""

  def volume(self, unit: Unit) -> Any:
    """Volume of an ingredient."""

  def temperature(self, unit: Unit) -> Any:
    """Cooking temperature."""


class MetricRecipe:
  """Uses metric measurements for recipes."""
  _system: MeasurementSystem = Metric()

  @property
  def system(self):
    return self._system

  @system.setter
  def system(self, system: MeasurementSystem):
    self._system = system

  def weight(self, unit: Unit) -> Grams:
    """Returns weight in grams."""
    return self.system.weight(unit)

  def volume(self, unit: Unit) -> mL:
    """Returns weight in grams."""
    return self.system.volume(unit)

  def temperature(self, unit: Unit) -> Celsius:
    """Returns weight in grams."""
    return self.system.temperature(unit)


class ImperialToMetricAdapter(Metric):
  """The Adapter ensures compatibility of imperial units in a recipe using metric units."""
  system = Imperial()

  def weight(self, unit: Unit) -> Grams:
    """Converts standard weight measurement to grams."""
    if not isinstance(unit, Grams):
      unit = Grams(454 * self.system.weight(unit).quantity)

    return unit

  def volume(self, unit: Unit) -> mL:
    """Converts standard volume measurement to mL."""
    if not isinstance(unit, mL):
      unit = mL(240 * self.system.volume(unit).quantity)

    return unit

  def temperature(self, unit: Unit) -> Celsius:
    """Converts standard temperature measurement to Celsius."""
    if not isinstance(unit, Celsius):
      unit = Celsius(5 / 9 * ((self.system.temperature(unit).quantity) - 32))
    return unit
