import pytest
from patterns.creational.abstract_factory.html_tag import HTMLElement, DarkModeHTML, LightModeHTML, ColorblindHTML


class TestAbstractFactory:

  def test_dark_mode_initialization(self):
    dark_mode_html = DarkModeHTML()
    assert dark_mode_html.html_elements == ["<html>"]
    element = dark_mode_html.add_element(
        HTMLElement.HEADING,
        html_content="Dark Mode HTML",
    )

    assert element.tag == "h1"
    assert f"{dark_mode_html}" == """<html>\n<h1 class='dark'>Dark Mode HTML</h1>\n</html>"""
    assert dark_mode_html.html_elements == [
        "<html>", "<h1 class='dark'>Dark Mode HTML</h1>"
    ]

  def test_light_mode_initialization(self):
    light_mode_html = LightModeHTML()
    assert light_mode_html.html_elements == ["<html>"]
    element = light_mode_html.add_element(
        HTMLElement.HEADING,
        html_content="Light Mode HTML",
    )

    assert element.tag == "h1"
    assert f"{light_mode_html}" == """<html>\n<h1 class='light'>Light Mode HTML</h1>\n</html>"""
    assert light_mode_html.html_elements == [
        "<html>", "<h1 class='light'>Light Mode HTML</h1>"
    ]

  def test_colorblind_initialization(self):
    colorblind_html = ColorblindHTML()
    assert colorblind_html.html_elements == ["<html>"]
    element = colorblind_html.add_element(
        HTMLElement.HEADING,
        html_content="Colorblind Mode HTML",
    )

    assert element.tag == "h1"
    assert f"{colorblind_html}" == """<html>\n<h1 class='colorblind'>Colorblind Mode HTML</h1>\n</html>"""
    assert colorblind_html.html_elements == [
        "<html>", "<h1 class='colorblind'>Colorblind Mode HTML</h1>"
    ]


if __name__ == "__main__":
  pytest.main([__file__])
