import pytest
from patterns.creational.builder.html_image import ImageBuilder, URL


class TestBuilder:

  @pytest.fixture
  def url(self):
    return URL("https://www.python_design_patterns.com/images/builder.png")

  def invalid_url(self, url: str):
    return False

  def test_url(self, url: URL):
    assert f"{url}" == "https://www.python_design_patterns.com/images/builder.png"

  def test_image(self, url: URL):
    regular_image = ImageBuilder()
    regular_image.set_source(url)
    assert f"{regular_image}" == "<img src='https://www.python_design_patterns.com/images/builder.png'></img>"
    assert repr(
        regular_image.element
    ) == "<img src='https://www.python_design_patterns.com/images/builder.png'></img>"

  def test_lazy_load_image(self, url: URL):
    lazyload_image = ImageBuilder()
    lazyload_image.set_source(url).set_lazyload().build()
    assert f"{lazyload_image}" == "<img src='https://www.python_design_patterns.com/images/builder.png' load='lazy'></img>"

  def test_lazy_load_image_thumbnail(self, url: URL):
    lazyload_thumbnail = ImageBuilder()
    lazyload_thumbnail.set_source(url).set_classes(
        "thumbnail").set_lazyload().build()
    assert f"{lazyload_thumbnail}" == "<img class='thumbnail' src='https://www.python_design_patterns.com/images/builder.png' load='lazy'></img>"

  def test_attributes(self, url: URL):
    image_with_attributes = ImageBuilder()
    image_with_attributes.set_source(url).set_id("hero").set_html_content(
        "Hero Image").build()

    assert image_with_attributes.element.html_attributes["id"] == "hero"
    assert image_with_attributes.element.content == "Hero Image"
    assert image_with_attributes.element.html_attributes[
        "src"] == "https://www.python_design_patterns.com/images/builder.png"

  def test_invalid_url(self):
    with pytest.raises(Exception):
      URL("fake_url", validator=self.invalid_url)


if __name__ == "__main__":
  pytest.main([__file__])
