from __future__ import annotations
import copy
from enum import Enum
from typing import Protocol


class Prototype(Protocol):
  """Prototype protocol that allows objects to be copied."""

  def clone(self):
    """Custom clone implementation."""
    clone = self.__class__()
    clone.__dict__.update(self.__dict__)
    return clone

  def copy(self):
    """Clone an object using Python's built-in copy library."""
    return copy.deepcopy(self)


class Image(Prototype):
  """Image data that implements the Prototype protocol."""
  aspect_ratio: tuple[int, int]
  height: int
  width: int
  url: str

  def __str__(self):
    return f"{self.image_url}({self.width} x {self.height} @{self.aspect_ratio[0]}:{self.aspect_ratio[1]})"

  @property
  def image_url(self):
    url = getattr(self, "url", "")
    return f"Image: {url} " if url else ""

  @property
  def resolution(self) -> tuple[int, int]:
    return (self.width, self.height)

  @resolution.setter
  def resolution(self, resolution: tuple[int, int]):
    self.width = resolution[0]
    self.height = resolution[1]


class ImagePrototype(Enum):
  """"Enumerated registry names for image prototypes."""
  SHV = "8K Super Hi-Vision"    #7680, 4320
  HV = "4K Hi-Vision"    #4096, 2160
  UHD = "Ultra High Definition"    #3840, 2160
  FHD = "Full High Definition"    #1920, 1080
  HD = "High Definition"    #1280, 720
  SD = "Standard Definition"    #720, 576

  def __str__(self):
    return self.value


class ImageRegistry:
  """Registry of image prototypes based on resolution."""
  registry: dict[ImagePrototype, Image]

  def __init__(self):
    self.registry = {}

  def __str__(self):
    return "\n".join([
        f"{image_format} Prototype Image {resolution}"
        for image_format, resolution in self.registry.items()
    ])

  def get_image_prototype(self, image_quality: ImagePrototype):
    """Returns an image prototype matching the enumeration passed."""
    return f"{image_quality} Prototype Image {self.registry[image_quality]}"

  def add_image_prototype(self, image_quality: ImagePrototype, image: Image):
    """Map an image prototype to its enumeration."""
    self.registry[image_quality] = image

  def new_image(self, image_quality: ImagePrototype):
    """Create a new image based on a prototype."""
    return self.registry[image_quality].clone()


image = Image()
registry = ImageRegistry()
image.aspect_ratio = 16, 9
image.resolution = 720, 576

registry.add_image_prototype(ImagePrototype.SD, image)

image.resolution = 1280, 720
registry.add_image_prototype(ImagePrototype.HD, image)

image.resolution = 1920, 1080
registry.add_image_prototype(ImagePrototype.FHD, image)

image.resolution = 3840, 2160
registry.add_image_prototype(ImagePrototype.UHD, image)

image.resolution = 7680, 4320
registry.add_image_prototype(ImagePrototype.SHV, image)

image.resolution = 4096, 2160
image.aspect_ratio = 256, 135
registry.add_image_prototype(ImagePrototype.HV, image)
print(registry)
