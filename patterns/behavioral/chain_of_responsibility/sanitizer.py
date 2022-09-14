"""Sanitizer uses the Chain of Responsibility design pattern to sanitize HTML.

Example Usage:
  text_input = "<script>alert('Executing malicious code')</script>"

  quote_sanitizer = QuoteSanitizer()
  tag_sanitizer = TagSanitizer()
  js_sanitizer = JavascriptSanitizer()

  quote_sanitizer.next_sanitizer(tag_sanitizer)
  tag_sanitizer.next_sanitizer(js_sanitizer)

  sanitized_input = quote_sanitizer.sanitize(text_input)

  print(sanitized_input)


Disclaimer: This module is for educational purposes only!
Do not use the following code to sanitize input in production.
"""
from __future__ import annotations
from abc import ABC, abstractmethod


class Sanitizer(ABC):
  """Sanitizer that prevents malicious code injection by users."""
  next: Sanitizer | None = None

  def next_sanitizer(self, sanitizer: Sanitizer):
    """Sets the next Sanitizer class in the Chain of Responsibility."""
    self.next = sanitizer

  @abstractmethod
  def sanitize(self, text_input: str) -> str:
    """Abstract sanitization method that renders potentially malicious code harmless."""


class QuoteSanitizer(Sanitizer):
  """Sanitizes quotes to prevent closing attributes prematurely and injecting code."""

  def sanitize(self, text_input: str) -> str:
    """Replaces quotes with character identity objects."""
    text_input = text_input.replace("\'", "&quot;").replace("\"", "&quot;")

    return self.next.sanitize(text_input) if self.next else text_input


class TagSanitizer(Sanitizer):
  """Sanitizes input to prevent creating HTML tags with open and close brackets."""

  def sanitize(self, text_input: str) -> str:
    """Replaces HTML open and close brackets with character identity objects."""
    text_input = text_input.replace("<", "&lt;").replace(">", "&gt;")

    return self.next.sanitize(text_input) if self.next else text_input


class JavascriptSanitizer(Sanitizer):
  """Sanitizes input to prevent running malicious Javascript code."""

  def sanitize(self, text_input: str) -> str:
    """Removes Javascript tags."""
    text_input = text_input.replace("<script>", "").replace("</script>", "")

    return self.next.sanitize(text_input) if self.next else text_input
