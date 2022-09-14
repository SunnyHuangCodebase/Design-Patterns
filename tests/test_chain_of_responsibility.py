import pytest

from patterns.behavioral.chain_of_responsibility.sanitizer import JavascriptSanitizer, QuoteSanitizer, TagSanitizer


class TestChainOfResponsibility:

  @pytest.fixture
  def quote_sanitizer(self):
    return QuoteSanitizer()

  @pytest.fixture
  def tag_sanitizer(self):
    return TagSanitizer()

  @pytest.fixture
  def js_sanitizer(self):
    return JavascriptSanitizer()

  def test_quote_sanitizer(self, quote_sanitizer: QuoteSanitizer):
    string = "'quoted text'"
    sanitized_string = quote_sanitizer.sanitize(string)
    assert sanitized_string == '&quot;quoted text&quot;'

  def test_tag_sanitizer(self, tag_sanitizer: TagSanitizer):
    string = "<h1 onclick='alert('Activated malicious code!')>"
    sanitized_string = tag_sanitizer.sanitize(string)
    assert sanitized_string == "&lt;h1 onclick='alert('Activated malicious code!')&gt;"

  def test_js_sanitizer(self, js_sanitizer: JavascriptSanitizer):
    string = "<script>Malicious code here</script>"
    sanitized_string = js_sanitizer.sanitize(string)
    assert sanitized_string == "Malicious code here"

  def test_chain_of_responsibility(self, quote_sanitizer: QuoteSanitizer,
                                   tag_sanitizer: TagSanitizer,
                                   js_sanitizer: JavascriptSanitizer):
    string = "Insert text here <script>alert('Executing malicious code')</script>"
    quote_sanitizer.next_sanitizer(tag_sanitizer)
    tag_sanitizer.next_sanitizer(js_sanitizer)
    sanitized_input = quote_sanitizer.sanitize(string)
    assert sanitized_input == "Insert text here &lt;script&gt;alert(&quot;Executing malicious code&quot;)&lt;/script&gt;"


if __name__ == "__main__":
  pytest.main([__file__])
