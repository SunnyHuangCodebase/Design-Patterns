"""Create HTML elements programmatically."""
from abc import ABC
from enum import Enum
from typing import Any


class Element(ABC):
  """Base HTML Element"""
  _attributes: dict[str, str]
  html_content: str
  tag: str

  def __init__(self, **attributes: str):
    """Initialize attribute keywords and values.
    
    Naming conventions:
      1. HTML element's class attribute (html_class) vs Python's built-in class (class)

        a. html_class = "centered" -> <{element} class="centered"></{elemnent}>

        b. class Element:
            ...

      2. HTML element's contents (html_content) vs HTML <meta>'s content attribute (content)

        a. html_content = "Text goes here." -> <{element}>Text goes here.</{element}>

        b. content = "Python Design Patterns" -> <meta content="Python Design Patterns">
      
      3. All other keyword parameters are identical to their HTML attribute names.
    """
    self._attributes: dict[str, str] = dict()

    # Map attribute and value of "id" before "class" to maintain HTML parse order.
    self._attributes["id"] = attributes.pop("id", "")

    # Convert invalid HTML attribute "html_class" parameter to "class" attribute.
    self._attributes["class"] = attributes.pop("html_class", "")

    # Separate inner HTML content from attributes.
    self.html_content = attributes.pop("html_content", "")

    # Remaining keyword arguments should all be valid HTML attributes.
    self._attributes |= attributes

  @property
  def attributes(self) -> str:
    """Parse attributes for opening HTML tag."""

    attributes = [
        f" {key}='{value}'" for key, value in self._attributes.items() if value
    ]
    return "".join(attributes)

  @property
  def open(self) -> str:
    """Return a properly formatted HTML opening tag along with its attributes."""
    return f"<{self.tag}{self.attributes}>"

  @property
  def close(self):
    """Return a property formatted HTML closing tag."""
    return f"</{self.tag}>"

  @property
  def html(self) -> str:
    """Return the object as HTML code."""
    return f"{self.open}{self.html_content}{self.close}"


class Heading(Element):
  """Generate an <h#> element, where # is a priority between 1-6.
  If no priority is specified, default to h1.
  """
  tag = "h"
  priority: str
  _attributes: dict[str, str]

  def __init__(self, **attributes: Any):
    priority = f"{attributes.pop('priority', '1')}"[0]
    try:
      priority = int(priority)
    except ValueError:
      print("ValueError: Heading elements have a priority value between 1-6.")
      raise
    priority = max(priority, 1)
    priority = min(priority, 6)
    self.tag += str(priority)
    super().__init__(**attributes)


class Div(Element):
  """Generate a <div> element."""
  tag = "div"


class Title(Element):
  """Generate a <title> element."""
  tag = "title"


class Image(Element):
  """Generate an <img> element."""
  tag = "img"


class HTMLElement(Enum):
  """Enumerated HTML Elements with callable members for instantiation."""
  TITLE = Title
  HEADING = Heading
  DIV = Div
  IMAGE = Image

  def __call__(self, *args: Any, **kwargs: Any):
    return self.value(*args, **kwargs)
