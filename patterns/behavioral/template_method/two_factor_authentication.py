from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import random
import string
from time import time


@dataclass
class User:
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
  code: str = field(default_factory=str)
  authorized: bool = False

  def authorization(self, user: User):
    """Template method to enable two-factor authentication."""
    self.generate_code()
    self.send_code(self.code, user)
    start_time = time()
    attempts = 0
    while not self.authorized and time() - start_time < 300 and attempts < 3:
      code = input()
      self.validate_code(code)
      attempts += 1

    return self.authorized

  def generate_code(self):
    """Generate a random six digit code."""
    self.code = "".join(random.choices(string.digits, k=6))

  @abstractmethod
  def send_code(self, code: str, user: User):
    """Sends code via user's authentication method."""

  @abstractmethod
  def obfuscate_user_info(self, user: User) -> str:
    """Partially hides user's personal identifying information."""

  def validate_code(self, code: str):
    """Checks if user entered the correct authorization code."""
    self.authorized = (code == self.code)


@dataclass
class TextAuthenticator(Authenticator):
  """Authenticates a user by sending a code through a text message."""

  def send_code(self, code: str, user: User):
    """Texts the code to the user's phone."""
    print(f"Sent a code to {self.obfuscate_user_info(user)}.")

  def obfuscate_user_info(self, user: User) -> str:
    return f"* (***) *** - **{user.phone[-2:]}"


@dataclass
class CallAuthenticator(Authenticator):
  """Authenticates a user by sending a code through a phone call."""

  def send_code(self, code: str, user: User):
    """Calls the user's phone to communicate the code through voice."""
    print(
        f"Calling in authentication code to {self.obfuscate_user_info(user)}.")

  def obfuscate_user_info(self, user: User) -> str:
    return f"* (***) *** - **{user.phone[-2:]}"


@dataclass
class EmailAuthenticator(Authenticator):
  """Authenticates a user by sending a code to their email address."""

  def send_code(self, code: str, user: User):
    """Emails the code to the user's email address."""
    print(f"Sent a code to {self.obfuscate_user_info(user)}.")

  def obfuscate_user_info(self, user: User) -> str:
    email, domain = user.email.split("@")
    first_letter = email[0]
    last_letter = email[-1]
    hidden = "*" * (len(email) - 2)
    return "".join([first_letter, hidden, last_letter, "@", domain])
