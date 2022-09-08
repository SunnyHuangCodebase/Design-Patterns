from __future__ import annotations
from abc import ABC, abstractmethod


class Interface(ABC):
  """How a webpage is presented to the user"""

  @abstractmethod
  def get_post_buttons(self) -> list[str]:
    """Get post UI elements."""

  @abstractmethod
  def get_comment_buttons(self) -> list[str]:
    """Get comment UI elements."""


class UserInterface(Interface):
  """"""

  def get_post_buttons(self) -> list[str]:
    """Get post UI elements."""
    return ["Read Later"]

  def get_comment_buttons(self) -> list[str]:
    """Get comment UI elements."""
    return ["Add Comment", "Reply to Comment"]


class AdminInterface(Interface):

  def get_post_buttons(self) -> list[str]:
    """Get post UI elements."""
    return ["Read Later", "Edit Post", "Delete Post"]

  def get_comment_buttons(self) -> list[str]:
    """Get comment UI elements."""
    return ["Add Comment", "Reply to Comment", "Delete Comment"]


class InsufficientPermissions(Exception):
  """Requested privileges exceed user's permissions."""


class Webpage(ABC):
  """Abstract webpage class."""

  def display_webpage(self):
    output = self.get_header()
    output.extend(self.get_post())
    output.extend(self.get_comments())
    output.extend(self.get_footer())
    return output

  def get_header(self):
    return ["Header"]

  def get_post(self):
    return ["Content"]

  def get_comments(self):
    return ["Comments"]

  def get_footer(self):
    return ["Footer"]


class UserWebpage(Webpage):
  """Webpage delivered to basic users."""

  def __init__(self, interface: UserInterface) -> None:
    if isinstance(interface, AdminInterface):
      raise InsufficientPermissions
    self.interface = interface

  def get_post(self):
    output = super().get_post()
    output.extend(self.interface.get_post_buttons())
    return output

  def get_comments(self):
    output = super().get_comments()
    output.extend(self.interface.get_comment_buttons())
    return output


class AdminWebpage(Webpage):
  """Webpage delivered to admins."""

  def __init__(self, interface: Interface):
    self.interface = interface

  def get_post(self):
    """Get post and buttons."""
    output = super().get_post()
    output.extend(self.interface.get_post_buttons())
    return output

  def get_comments(self):
    """Get comments and UI buttons"""
    output = super().get_comments()
    output.extend(self.interface.get_comment_buttons())
    return output
