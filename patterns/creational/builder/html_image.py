from __future__ import annotations
from abc import ABC
from typing import Any, Callable


class HTMLElement(ABC):
  """Abstract HTML element."""
  tag: str
  html_attributes: dict[str, str]
  content: str

  def __repr__(self):
    return self.html

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

  def __repr__(self) -> str:
    return self.element.html

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

  def __new__(cls, url, validator: Callable[[str], bool] = always_valid):
    """Validates URL and returns whether it is valid."""
    if not validator(url):
      raise Exception("Invalid URL")

    return super().__new__(cls, url)

  def __init__(self, url: str, *_):
    self.url = url
    super().__init__()

  def __str__(self):
    return self.url


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
