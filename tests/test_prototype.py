from textwrap import dedent
import pytest
from patterns.creational.prototype.image import Image, ImagePrototype, ImageRegistry


class TestPrototype:

  @pytest.fixture
  def registry(self):
    """Initialize all image prototypes."""
    image = Image()
    registry = ImageRegistry()

    image.resolution = 720, 576
    image.aspect_ratio = 16, 9
    registry.add_image_prototype(ImagePrototype.SD, image)

    hd_image = image.clone()
    hd_image.resolution = 1280, 720
    registry.add_image_prototype(ImagePrototype.HD, hd_image)

    fhd_image = image.clone()
    fhd_image.resolution = 1920, 1080
    registry.add_image_prototype(ImagePrototype.FHD, fhd_image)

    uhd_image = image.clone()
    uhd_image.resolution = 3840, 2160
    registry.add_image_prototype(ImagePrototype.UHD, uhd_image)

    hv_image = image.clone()
    hv_image.resolution = 4096, 2160
    hv_image.aspect_ratio = 256, 135
    registry.add_image_prototype(ImagePrototype.HV, hv_image)

    shv_image = image.clone()
    shv_image.resolution = 7680, 4320
    registry.add_image_prototype(ImagePrototype.SHV, shv_image)

    return registry

  def test_image_copy(self):
    image = Image()
    image.resolution = 720, 576
    assert image.resolution == (720, 576)
    image_clone = image.clone()
    image_copy = image.copy()
    assert image_copy.__dict__ == image_clone.__dict__ == image.__dict__

  def test_prototype_creation(self):
    image = Image()
    registry = ImageRegistry()
    image.aspect_ratio = 16, 9
    image.resolution = 720, 576

    registry.add_image_prototype(ImagePrototype.SD, image)
    assert registry.registry[ImagePrototype.SD] == image

  def test_image_registry(self, registry: ImageRegistry):
    image = registry.registry[ImagePrototype.SD]
    assert image.resolution == (720, 576)
    assert image.aspect_ratio == (16, 9)

    image = registry.registry[ImagePrototype.HD]
    assert image.resolution == (1280, 720)
    assert image.aspect_ratio == (16, 9)

    image = registry.registry[ImagePrototype.FHD]
    assert image.resolution == (1920, 1080)
    assert image.aspect_ratio == (16, 9)

    image = registry.registry[ImagePrototype.UHD]
    assert image.resolution == (3840, 2160)
    assert image.aspect_ratio == (16, 9)

    image = registry.registry[ImagePrototype.HV]
    assert image.resolution == (4096, 2160)
    assert image.aspect_ratio == (256, 135)

    image = registry.registry[ImagePrototype.SHV]
    assert image.resolution == (7680, 4320)
    assert image.aspect_ratio == (16, 9)

  def test_get_image_prototype(self, registry: ImageRegistry):
    assert registry.get_image_prototype(
        ImagePrototype.SHV
    ) == "8K Super Hi-Vision Prototype Image (7680 x 4320 @16:9)"

  def test_registry_str(self, registry: ImageRegistry):
    registry_string = dedent("""\
    Standard Definition Prototype Image (720 x 576 @16:9)
    High Definition Prototype Image (1280 x 720 @16:9)
    Full High Definition Prototype Image (1920 x 1080 @16:9)
    Ultra High Definition Prototype Image (3840 x 2160 @16:9)
    4K Hi-Vision Prototype Image (4096 x 2160 @256:135)
    8K Super Hi-Vision Prototype Image (7680 x 4320 @16:9)""")

    assert f"{registry}" == registry_string

  def test_prototype_image_creation(self, registry: ImageRegistry):
    new_shv_image = registry.new_image(ImagePrototype.SHV)
    assert new_shv_image.__dict__ == registry.registry[
        ImagePrototype.SHV].__dict__
    new_shv_image.url = "https://www.python-design-patterns.com/images/builder.png"


if __name__ == "__main__":
  pytest.main([__file__])
