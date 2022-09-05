from patterns.creational.factory.html_element import Element, HTMLElement


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


if __name__ == "__main__":

  html = HTMLGenerator()

  html.add_element(
      HTMLElement.TITLE,
      html_content="Python Factory Design Pattern",
  )

  html.add_element(
      HTMLElement.HEADING,
      id="title",
      html_content="Python Factory Design Pattern?",
  )

  html.add_element(
      HTMLElement.HEADING,
      priority=2,
      html_content="Factory Design Pattern Example",
  )

  html.add_element(
      HTMLElement.IMAGE,
      html_class="thumbnail",
      loading="lazy",
      src="https://www.python-design-patterns.com/images/factory-pattern.png",
      alt="Factory Pattern UML Diagram",
  )

  html.add_element(
      HTMLElement.DIV,
      html_content="The factory design pattern separates creation from use.",
  )

  print(html)
