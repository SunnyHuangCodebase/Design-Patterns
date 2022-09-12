from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pympler.asizeof import asizeof    #type: ignore


@dataclass
class Pixel:
  """Generic Pixel."""

  red: int
  blue: int
  green: int
  opacity: int


class BasePixelFactory(ABC):
  """Base Pixel Class"""
  red: int
  blue: int
  green: int
  opacity: int

  @abstractmethod
  def get_pixel(self,
                red: int,
                blue: int,
                green: int,
                opacity: int = 256) -> Pixel:
    """Returns a Pixel"""


class PixelFactory(BasePixelFactory):
  """Pixel Factory to return Pixel objects."""

  def get_pixel(self,
                red: int,
                blue: int,
                green: int,
                opacity: int = 256) -> Pixel:
    return Pixel(red, blue, green, opacity)


class FlyweightPixelFactory(BasePixelFactory):
  """Factory that returns flyweight Pixel objects."""
  pixels: dict[int, Pixel]

  def __init__(self):
    self.pixels = {}

  def generate_unique_pixel_key(self, red: int, blue: int, green: int,
                                opacity: int):
    """Generate a key for a flyweight pixel hashmap."""
    return sum([red * 1_000_000_000, blue * 1_000_000, green * 1_000, opacity])

  def get_pixel(self,
                red: int,
                blue: int,
                green: int,
                opacity: int = 256) -> Pixel:
    """Returns a flyweight pixel if it exists, otherwise create one."""
    key = self.generate_unique_pixel_key(red, blue, green, opacity)
    pixel = self.pixels.get(key, None)

    if not pixel:
      pixel = Pixel(red, blue, green, opacity)
      self.pixels[key] = pixel

    return pixel


class Portrait:
  """An image that contains pixels"""
  board: list[list[Pixel | None]]
  factory: BasePixelFactory
  pixel_list: list[Pixel] = []

  def __init__(self, rows: int, columns: int,
               factory: BasePixelFactory) -> None:
    self.board = [[None for _ in range(columns)] for _ in range(rows)]
    self.factory = factory

  def render_white_pixel_image(self):
    """Create an image with a all white pixels."""
    for row in range(len(self.board)):
      for col in range(len(self.board[0])):
        self.board[row][col] = self.factory.get_pixel(256, 256, 256)
