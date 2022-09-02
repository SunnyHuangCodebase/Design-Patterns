from patterns.creational.abstract_factory.html_element import HTMLElement, Element


class HTMLGenerator:
  """HTML Factory"""
  html_elements: list[str]

  def __init__(self):
    self.html_elements = ["<html>"]

  def __str__(self):
    return self.output

  def add_element(self,
                  element: HTMLElement,
                  *,
                  priority: int = 0,
                  **attributes: str):
    """Create HTML element based on the enumerated HTMLElement member passed."""
    # Priority is only required for heading elements (h1-h6).
    if element is HTMLElement.HEADING:
      attributes["priority"] = str(priority or 1)

    html_element: Element = element(**attributes)
    self.html_elements.append(html_element.html)
    return html_element

  @property
  def output(self):
    return "\n".join([*self.html_elements, "</html>"])


class DarkModeHTML(HTMLGenerator):
  """Dark Mode HTML Factory."""

  def add_element(self,
                  element: HTMLElement,
                  *,
                  priority: int = 0,
                  **attributes: str):
    classes = attributes.get("html_class", "")
    attributes["html_class"] = classes + " dark" if classes else "dark"
    return super().add_element(element, priority=priority, **attributes)


class LightModeHTML(HTMLGenerator):
  """Light Mode HTML Factory."""

  def add_element(self,
                  element: HTMLElement,
                  *,
                  priority: int = 0,
                  **attributes: str):

    classes = attributes.get("html_class", "")
    attributes["html_class"] = classes + " light" if classes else "light"
    return super().add_element(element, priority=priority, **attributes)


class ColorblindHTML(HTMLGenerator):

  def add_element(self,
                  element: HTMLElement,
                  *,
                  priority: int = 0,
                  **attributes: str):
    classes = attributes.get("html_class", "")
    attributes[
        "html_class"] = classes + " colorblind" if classes else "colorblind"
    return super().add_element(element, priority=priority, **attributes)
