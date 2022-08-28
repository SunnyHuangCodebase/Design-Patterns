from Factory.html_elements import HTMLElement
from Factory.html_factory import HTMLGenerator


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


if __name__ == "__main__":

  dark_mode_html = DarkModeHTML()
  light_mode_html = LightModeHTML()
  colorblind_mode_html = ColorblindHTML()

  dark_mode_html.add_element(
      HTMLElement.TITLE,
      html_content="Dark Mode HTML",
  )

  light_mode_html.add_element(
      HTMLElement.TITLE,
      html_content="Light Mode HTML",
  )

  colorblind_mode_html.add_element(
      HTMLElement.TITLE,
      html_content="Colorblind Mode HTML",
  )

  print(dark_mode_html)
  print(light_mode_html)
  print(colorblind_mode_html)
