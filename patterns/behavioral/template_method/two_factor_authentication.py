"""The Authenticator implements the Template Method design pattern.

The Authenticator class is an abstract base class containing a "template" for subclasses.
The template may include a combination of template methods, abstract methods, and hooks.

Template methods: Authorization template method which all subclasses can call.

Abstract methods: Obfuscate user abstract method that subclasses must implement.
  It partially hides contact information to which the authentication code was sent.

Hooks: A generate_code method with default behavior, which can be overridden in subclasses.
  For example, generate_code may generate a QR code instead of a 6 digit code.)

"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random
import string
from time import time


@dataclass
class User:
  """A user of any particular app."""
  phone: str
  email: str
  two_factor_authentication: bool

  def confirm_identity(self, authenticator: Authenticator):
    """If two factor authentication enabled, confirm user's identity upon login."""

    if self.two_factor_authentication and not authenticator.authorization(self):
      print("Please try logging in again!")
    else:
      print("Successfully logged in!")


class Authenticator(ABC):
  """Verifies a login is valid via authentication method specified by the user."""
  code: str = field(default_factory=str)
  authorized: bool = False

  def authorization(self, user: User):
    """Template method to enable two-factor authentication."""
    self._generate_code()
    self._send_code(self.code, user)
    start_time = time()
    attempts = 0
    while not self.authorized and time() - start_time < 300 and attempts < 3:
      code = input()
      self._validate_code(code)
      attempts += 1

    return self.authorized

  def _generate_code(self):
    """A hook that generates a random six digit code, which can be overriden for alternate codes."""
    self.code = "".join(random.choices(string.digits, k=6))

  @abstractmethod
  def _send_code(self, code: str, user: User):
    """Sends code via user's authentication method."""

  @abstractmethod
  def _obfuscate_user_info(self, user: User) -> str:
    """Partially hides user's personal identifying information."""

  def _validate_code(self, code: str):
    """Checks if user entered the correct authorization code."""
    self.authorized = (code == self.code)


@dataclass
class TextAuthenticator(Authenticator):
  """Authenticates a user by sending a code through a text message."""

  def _send_code(self, code: str, user: User):
    """Texts the code to the user's phone."""
    print(f"Sent a code to {self._obfuscate_user_info(user)}.")

  def _obfuscate_user_info(self, user: User) -> str:
    return f"* (***) *** - **{user.phone[-2:]}"


@dataclass
class CallAuthenticator(Authenticator):
  """Authenticates a user by sending a code through a phone call."""

  def _send_code(self, code: str, user: User):
    """Calls the user's phone to communicate the code through voice."""
    print(
        f"Calling in authentication code to {self._obfuscate_user_info(user)}.")

  def _obfuscate_user_info(self, user: User) -> str:
    return f"* (***) *** - **{user.phone[-2:]}"


@dataclass
class EmailAuthenticator(Authenticator):
  """Authenticates a user by sending a code to their email address."""

  def _send_code(self, code: str, user: User):
    """Emails the code to the user's email address."""
    print(f"Sent a code to {self._obfuscate_user_info(user)}.")

  def _obfuscate_user_info(self, user: User) -> str:
    email, domain = user.email.split("@")
    first_letter = email[0]
    last_letter = email[-1]
    hidden = "*" * (len(email) - 2)
    return "".join([first_letter, hidden, last_letter, "@", domain])
