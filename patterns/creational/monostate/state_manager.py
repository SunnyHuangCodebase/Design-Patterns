from __future__ import annotations
from threading import Lock
from typing import Any
from time import sleep


class StateManager:
  """A Monostate application state manager."""
  _state: dict[str, Any] = {}
  history: list[str]
  future: list[str]
  _lock = Lock()

  def __new__(cls, *args: Any, **kwargs: Any):
    """Creates a new instance of StateManager whose __dict__ references the class _state dictionary."""
    instance = super().__new__(cls, *args, **kwargs)
    instance.__dict__ = cls._state
    return instance

  def __init__(self):
    self.history = getattr(self, "history", [])
    self.future = getattr(self, "future", [])

  def add_state(self, value: str):
    """Adds a new application state and removes future states."""
    self.history.append(value)
    self.future.clear()

  def undo(self):
    """Removes the most recent application state and puts it into future."""
    if self.history:
      sleep(1)
      self.future.append(self.history.pop())

  def redo(self):
    """Adds the most recently removed state as the most recent application state."""
    if self.future:
      self.history.append(self.future.pop())

  def clear(self):
    self.history.clear()
    self.future.clear()

  @property
  def current_state(self):
    """Return the most recent application state."""
    return self.history[-1]
