import pytest
from patterns.creational.abstract_factory.html_element import Heading, HTMLElement


class TestHTMLElement:

  def test_heading_default(self):
    """Test heading initilization without arguments."""
    heading = Heading()
    assert heading.tag == "h1"
    assert heading.attributes == ""

  def test_heading_tag(self):
    """Test heading tag."""
    heading = Heading(priority=1)
    assert heading.tag == "h1"
    assert heading.open == "<h1>"
    assert heading.close == "</h1>"

    heading = Heading(priority="2")
    assert heading.tag == "h2"
    assert heading.open == "<h2>"
    assert heading.close == "</h2>"

  def test_heading_priority_out_of_range(self):
    """Test headings initialized with out of bound priorities."""
    heading = Heading(priority="0")
    assert heading.tag == "h1"

    heading = Heading(priority=99)
    assert heading.tag == "h6"

  def test_heading_priority_invalid(self):
    """Test headings initialized with invalid priority."""
    with pytest.raises(ValueError):
      heading = Heading(priority="a")

    heading = Heading(priority="1 script='injection.js'")
    assert heading.tag == "h1"
    assert heading.open == "<h1>"
    assert heading.close == "</h1>"

  def test_heading_attributes(self):
    """Test headings initialized with attributes."""
    heading1 = Heading(id="heading")
    assert heading1.attributes == " id='heading'"

    heading2 = Heading(html_class="heading")
    assert heading2.attributes == " class='heading'"

    heading3 = Heading(html_class="heading bold", style="style.css")
    assert heading3.attributes == " class='heading bold' style='style.css'"

  def test_enumeration_call(self):
    heading = HTMLElement.HEADING(html_class="heading")
    assert isinstance(heading, Heading)
    assert heading.tag == "h1"
    assert heading.open == "<h1 class='heading'>"
    assert heading.close == "</h1>"
    assert heading.attributes == " class='heading'"


if __name__ == "__main__":
  pytest.main([__file__])
