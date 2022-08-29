from __future__ import annotations
from abc import ABC
from typing import Callable


class HTMLElement(ABC):
  """Abstract HTML element."""
  tag: str
  html_attributes: dict[str, str]
  content: str

  @property
  def attributes(self) -> str:
    return "".join([
        f" {key}='{value}'" for key, value in self.html_attributes.items()
        if value
    ])

  @property
  def html(self) -> str:
    return f"<{self.tag}{self.attributes}>{self.content}</{self.tag}>"


class Image(HTMLElement):
  """Image HTML element"""
  tag = "img"
  html_attributes: dict[str, str] = {
      "id": "",
      "class": "",
      "src": "",
      "alt": "",
      "width": "",
      "height": "",
  }
  content = ""


class HTMLBuilder(ABC):
  """Abstract builder to create HTML objects."""
  element: HTMLElement

  def set_id(self, id: str):
    """Sets unique id selector."""
    self.element.html_attributes["id"] = id
    return self

  def set_classes(self, *classes: str):
    """Sets one or more class selectors."""
    self.element.html_attributes["class"] = " ".join(classes)
    return self

  def set_html_content(self, content: str):
    """Sets content contained within HTML tags."""
    self.element.content = content
    return self

  def build(self):
    """Returns the HTML element as a parsed HTML string."""
    return self.element.html


def always_valid(url: str):
  """Dummy validator that assesses a non-zero length string as a valid URL."""
  return bool(url)


class URL(str):
  """A URL string."""

  def __init__(self, url: str) -> None:
    self.url = url
    super().__init__()

  def __str__(self):
    if self.is_valid():
      return self.url
    raise Exception("Invalid URL")

  def is_valid(self, validator: Callable[[str], bool] = always_valid):
    """Validates URL and returns whether it is valid."""
    return validator(self.url)


class ImageBuilder(HTMLBuilder):
  """Builder for the HTML tag <img>."""

  def __init__(self):
    self.element = Image()

  def set_source(self, value: URL):
    self.element.html_attributes["src"] = value
    return self

  def set_lazyload(self):
    self.element.html_attributes["load"] = "lazy"
    return self


if __name__ == "__main__":

  url = URL("https://www.python_design_patterns.com/images/builder.png")
  regular_image = ImageBuilder()
  regular_image.set_source(url).build()
  print(regular_image)

  lazyload_image = ImageBuilder()
  lazyload_image.set_source(url).set_lazyload().build()
  print(lazyload_image)

  lazyload_thumbnail = ImageBuilder()
  lazyload_thumbnail.set_source(url).set_classes(
      "thumbnail").set_lazyload().build()
  print(lazyload_thumbnail)
