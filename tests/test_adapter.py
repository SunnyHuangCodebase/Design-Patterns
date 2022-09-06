import pytest
from patterns.structural.adapter.recipe_measurements import (
    Celsius, Cups, Fahrenheit, Imperial, IncorrectUnit, Grams, Pounds,
    ImperialToMetricAdapter, MetricRecipe, mL)


class TestAdapter:

  def test_compatible_interface(self):
    """Test metric units in a metric recipe."""
    recipe = MetricRecipe()

    weight = Grams(454)
    weight = recipe.weight(weight)
    assert weight.quantity == 454
    assert weight.name == "grams"

    volume = mL(240)
    volume = recipe.volume(volume)
    assert volume.quantity == 240
    assert volume.name == "mL"

    temperature = Celsius(100)
    temperature = recipe.temperature(temperature)
    assert temperature.quantity == 100
    assert temperature.name == "Celsius"

  def test_incompatible_interface(self):
    """Test imperial units in a metric recipe."""
    metric_recipe = MetricRecipe()
    weight = Pounds(1)
    with pytest.raises(IncorrectUnit):
      metric_recipe.weight(weight)

    volume = Cups(1)
    with pytest.raises(IncorrectUnit):
      metric_recipe.volume(volume)

    temperature = Fahrenheit(212)
    with pytest.raises(IncorrectUnit):
      metric_recipe.temperature(temperature)

    imperial = Imperial()
    weight = Grams(1)
    with pytest.raises(IncorrectUnit):
      imperial.weight(weight)

    volume = mL(1)
    with pytest.raises(IncorrectUnit):
      imperial.volume(volume)

    temperature = Celsius(212)
    with pytest.raises(IncorrectUnit):
      imperial.temperature(temperature)

  def test_adapter_interface(self):
    """Test imperial units in a metric recipe with an adapter."""
    metric_recipe = MetricRecipe()
    adapter = ImperialToMetricAdapter()
    metric_recipe.system = adapter

    weight = Pounds(1)
    weight = metric_recipe.weight(weight)
    assert weight.quantity == 454
    assert weight.name == "grams"

    volume = Cups(1)
    volume = metric_recipe.volume(volume)
    assert volume.quantity == 240
    assert volume.name == "mL"

    temperature = Fahrenheit(212)
    temperature = metric_recipe.temperature(temperature)
    assert temperature.quantity == 100
    assert temperature.name == "Celsius"


if __name__ == "__main__":
  pytest.main([__file__])
