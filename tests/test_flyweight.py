import pytest

from pympler.asizeof import asizeof    #type: ignore

from patterns.structural.flyweight.pixel import FlyweightPixelFactory, PixelFactory, Portrait


class TestFlyWeight:

  @pytest.fixture
  def factory(self) -> PixelFactory:
    return PixelFactory()

  @pytest.fixture
  def flyweight_factory(self) -> FlyweightPixelFactory:
    return FlyweightPixelFactory()

  @pytest.fixture
  def portrait(self, factory: PixelFactory):
    return Portrait(100, 100, factory)

  @pytest.fixture
  def flyweight_portrait(self, flyweight_factory: FlyweightPixelFactory):
    return Portrait(100, 100, flyweight_factory)

  def test_pixel_factory(self, factory: PixelFactory):
    """Ensure PixelFactory correctly instantiates a Pixel."""
    pixel = factory.get_pixel(256, 256, 256, 256)
    assert pixel.red == 256
    assert pixel.blue == 256
    assert pixel.green == 256
    assert pixel.opacity == 256

  def test_flyweight_pixel_factory(self,
                                   flyweight_factory: FlyweightPixelFactory):
    """Ensure FlyweightPixelFactory correctly instantiates a Pixel."""
    flyweight_pixel = flyweight_factory.get_pixel(256, 256, 256, 256)
    assert flyweight_pixel.red == 256
    assert flyweight_pixel.blue == 256
    assert flyweight_pixel.green == 256
    assert flyweight_pixel.opacity == 256

  def test_default_pixel_opacity(self, factory: PixelFactory,
                                 flyweight_factory: FlyweightPixelFactory):
    """Pixel opacity automatically set to 256."""
    pixel = factory.get_pixel(256, 256, 256)
    assert pixel.opacity == 256
    pixel = flyweight_factory.get_pixel(256, 256, 256)
    assert pixel.opacity == 256

  def test_pixel_instances(self, factory: PixelFactory):
    """Pixel factory returns a new Pixel even if it is a duplicate."""
    pixel1 = factory.get_pixel(256, 256, 256)
    pixel2 = factory.get_pixel(256, 256, 256)
    assert pixel1 == pixel2
    assert id(pixel1) != id(pixel2)

  def test_flyweight_pixels(self, flyweight_factory: FlyweightPixelFactory):
    """Flyweight factory returns existing Pixel where it would otherwise create a duplicate."""
    pixel1 = flyweight_factory.get_pixel(256, 256, 256)
    pixel2 = flyweight_factory.get_pixel(256, 256, 256)
    assert pixel1 == pixel2
    assert id(pixel1) == id(pixel2)

  def test_portrait_sizes(self, portrait: Portrait,
                          flyweight_portrait: Portrait):
    """Portraits with a FlyweightPixelFactory uses < 10% the memory of one with a PixelFactory."""
    portrait.render_white_pixel_image()
    flyweight_portrait.render_white_pixel_image()

    assert asizeof(portrait.board) > 10 * asizeof(flyweight_portrait.board)


if __name__ == "__main__":
  pytest.main([__file__])
