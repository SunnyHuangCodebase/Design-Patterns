from textwrap import dedent
import pytest
from patterns.structural.composite.html_generator import NodeElement, LeafElement


class TestComposite:

  def test_node_element(self):
    """"""
    html = NodeElement(tag="html")
    assert html.tag == "html"
    assert html.html_content == ""
    assert html.html_output() == dedent("""\
      <html>
      </html>""")

  def test_leaf_element(self):
    title = LeafElement(tag="title", html_content="Title")
    assert title.tag == "title"
    assert title.html_content == "Title"
    assert title.html_output() == "<title>Title</title>"

  def test_composite_element(self):
    """"""
    html = NodeElement(tag="html")
    title = LeafElement(tag="title", html_content="Title")
    html.add_child(title)
    assert html.html_output() == dedent("""\
      <html>
        <title>Title</title>
      </html>""")

  def test_multi_tier_composite_structure(self):
    """"""
    html = NodeElement(tag="html")
    title = LeafElement(tag="title", html_content="Title")
    body = NodeElement(tag="body")
    article = NodeElement(tag="article")
    heading = LeafElement(tag="h1", html_content="Composite Design Pattern")
    p = NodeElement(tag="p", html_content="Introduction to Composite Pattern.")

    html.add_child(title)
    html.add_child(body)

    body.add_child(article)

    article.add_child(heading)
    article.add_child(p)

    assert html.html_output() == dedent("""\
      <html>
        <title>Title</title>
        <body>
          <article>
            <h1>Composite Design Pattern</h1>
            <p>
              Introduction to Composite Pattern.
            </p>
          </article>
        </body>
      </html>""")


if __name__ == "__main__":
  pytest.main([__file__])
