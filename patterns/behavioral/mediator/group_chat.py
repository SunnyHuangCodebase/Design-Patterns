from __future__ import annotations
from dataclasses import dataclass, field


class MessengerFactory:
  """Handles creating users and chats."""

  def create_user(self, id: int, username: str) -> User:
    """Returns a User instance."""
    return User(id, username)

  def create_chat(self, id: int, chat_name: str) -> GroupChat:
    """Returns a Chat instance."""
    return GroupChat(id, chat_name)


class Database:
  """Database of users and chats."""
  factory: MessengerFactory
  users: dict[int, User]
  last_user_id: int = 0
  chats: dict[int, GroupChat]
  last_chat_id: int = 0

  def __init__(self, factory: MessengerFactory):
    self.factory = factory
    self.users = {}
    self.chats = {}

  def new_user(self, username: str):
    """Creates a user and adds it to the database."""
    id = self.next_user_id()
    user = self.factory.create_user(id, username)
    self.users[id] = user
    return user

  def new_chat(self, chat_name: str):
    """Creates a chat and adds it to the database."""
    id = self.next_chat_id()
    chat = self.factory.create_chat(id, chat_name)
    self.chats[id] = chat
    return chat

  def next_user_id(self) -> int:
    """Generates and returns the next available user ID."""
    self.last_user_id += 1
    return self.last_user_id

  def next_chat_id(self) -> int:
    """Generates and returns the next available chat ID."""
    self.last_chat_id += 1
    return self.last_chat_id


@dataclass
class GroupChat:
  """Chat implementing the Mediator design pattern to allow user communication."""
  id: int
  name: str
  participants: list[User] = field(default_factory=list)

  def add_participant(self, user: User):
    """Adds a user to the group chat."""
    if user in self.participants:
      return

    self.participants.append(user)
    user.set_current_chat(self)

  def send_message(self, message: str, sender: User):
    """Sends message to all participants."""
    for user in self.participants:
      user.receive_message(message, sender)


class User:
  """User object consisting of unique user ID and a username."""
  id: int
  name: str
  inbox: list[str]
  chat: GroupChat

  def __init__(self, id: int, name: str) -> None:
    self.id = id
    self.name = name
    self.inbox = []

  def __str__(self):
    return self.name

  def set_current_chat(self, chat: GroupChat):
    """Sets chat as the mediator for all group chat participants."""
    self.chat = chat

  def send_group_message(self, message: str):
    """Sends a message to the group chat."""
    self.chat.send_message(message, self)

  def receive_message(self, message: str, sender: User):
    """Adds incoming group chat messages to the inbox."""
    self.inbox.append(f"{sender}: {message}")

  def display_messages(self):
    """Shows all group chat messages."""
    return "\n".join(self.inbox)
