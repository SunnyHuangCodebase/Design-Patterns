from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class HTMLElement(ABC):
  """Base HTML Element"""
  _attributes: dict[str, str]
  tag: str
  html_content: str
  delimiter: str = "  "

  def __init__(self, **attributes: str):
    self._attributes: dict[str, str] = dict()
    self._attributes["id"] = attributes.pop("id", "")
    self._attributes["class"] = attributes.pop("html_class", "")
    self.html_content = attributes.pop("html_content", "")
    self._attributes |= attributes

  @property
  def attributes(self) -> str:
    """Parse attributes for opening HTML tag."""

    attributes = [
        f" {key}='{value}'" for key, value in self._attributes.items() if value
    ]
    return "".join(attributes)

  @abstractmethod
  def open(self, level: int = 0) -> str:
    """Return formatted HTML opening tag and its attributes."""

  @abstractmethod
  def close(self, level: int = 0) -> str:
    """Return formatted HTML closing tag."""

  @abstractmethod
  def content(self, level: int = 0) -> str:
    """Return properly formatted content."""

  @abstractmethod
  def html_output(self, level: int = 0) -> str:
    """Return the object as HTML code."""


class NodeElement(HTMLElement):
  """A generic HTML element that may have children. Output is multi-tiered."""
  children: list[HTMLElement]

  def __init__(self, **attributes: str):
    self.tag = attributes.pop("tag", "")
    self.children = []
    super().__init__(**attributes)

  def add_child(self, element: HTMLElement):
    """Adds a child HTML Element"""
    self.children.append(element)

  def open(self, level: int = 0) -> str:
    """Return formatted HTML opening tag and its attributes."""
    delimiter = self.delimiter * level
    return f"{delimiter}<{self.tag}{self.attributes}>"

  def close(self, level: int = 0) -> str:
    """Return formatted HTML closing tag."""
    delimiter = self.delimiter * level
    return f"{delimiter}</{self.tag}>"

  def content(self, level: int = 0) -> str:
    """Return properly formatted content."""
    return f"{(1 + level) * self.delimiter}{self.html_content}"

  def html_output(self, level: int = 0) -> str:
    """Return the object as HTML code."""
    output = [self.open(level)]

    if self.html_content:
      output.append(self.content(level))

    for child in self.children:
      output.append(f"{child.html_output(level + 1)}")

    output.append(self.close(level))
    return "\n".join(output)


class LeafElement(HTMLElement):
  """A generic HTML element without any children. Output is a single line."""

  def __init__(self, **attributes: str):
    self.tag = attributes.pop("tag", "")
    super().__init__(**attributes)

  def open(self, *_: Any) -> str:
    """Return formatted HTML opening tag and its attributes."""
    return f"<{self.tag}{self.attributes}>"

  def close(self, *_: Any) -> str:
    """Return formatted HTML closing tag."""
    return f"</{self.tag}>"

  def content(self, *_: Any) -> str:
    return f"{self.html_content}"

  def html_output(self, level: int = 0) -> str:
    """Return the object as HTML code."""
    return f"{self.delimiter * level}{self.open()}{self.content()}{self.close()}"
