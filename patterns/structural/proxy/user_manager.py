from __future__ import annotations
from dataclasses import dataclass
from enum import Enum


class UserPermissionLevel(int, Enum):
  SYSTEM = 5
  ADMIN = 4
  MODERATOR = 3
  AUTHOR = 2
  USER = 1


class InsufficientPermissions(Exception):
  """User action exceeds permission level."""


class Inbox:
  messages: list[str]

  def __init__(self, messages: list[str] | None = None) -> None:
    self.messages = messages or []

  def receive_message(self, message: str):
    self.messages.append(message)


@dataclass
class User:
  """A user of an App."""
  name: str
  permissions: UserPermissionLevel
  banned: bool = False
  infractions: int = 0
  inbox: Inbox = Inbox()

  def __str__(self):
    return self.name

  def ban_user(self):
    """Sets banned attribute to True, preventing the user from using the app."""
    self.banned = True
    self.inbox.receive_message("You have been banned from using the app.")


@dataclass
class App:
  """A service consisting of a user manager and other features."""
  manager: UserManager

  def ban(self, requestor: User, user: User):
    """Sends a ban request."""
    try:
      self.manager.ban(requestor, user)
    except InsufficientPermissions:
      raise


class UserManager:
  """Handles requests such as creating, warning, reporting, and banning users."""
  log: Log

  def ban(self, requestor: User, user: User):
    """Bans a user from using the App."""
    if requestor.permissions < UserPermissionLevel.ADMIN:
      raise InsufficientPermissions
    user.ban_user()


@dataclass
class LoggingUserManager(UserManager):
  """A proxy object that logs all user management actions."""
  manager: UserManager
  log: Log

  def log_action(self, requestor: User, user: User, action: str):
    """Logs the request to the logger."""
    self.log.log_action(f"{requestor} has {action} {user}.")

  def ban(self, requestor: User, user: User):
    """Ban a user from using the App."""
    try:
      super().ban(requestor, user)
      self.log_action(requestor, user, "banned")
    except InsufficientPermissions:
      raise


class Log:
  history: list[str]

  def __init__(self) -> None:
    self.history = []

  def log_action(self, log_message: str):
    """Adds the log message to log history."""
    self.history.append(log_message)
