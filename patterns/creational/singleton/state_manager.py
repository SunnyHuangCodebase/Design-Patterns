from __future__ import annotations
from threading import Lock
from typing import Any, Callable
from time import sleep


def thread_lock():
  """Thread lock decorator."""
  lock = Lock()

  def decorator(function: Callable[..., Any]):

    def wrapper(*args: Any, **kwargs: Any):
      with lock:
        function(*args, **kwargs)

    return wrapper

  return decorator


class StateManager:
  """A Singleton application state manager."""
  instance: StateManager
  history: list[str]
  future: list[str]
  _lock = Lock()

  def __new__(cls):
    """Allows instantiation of only one Singleton object and returns it."""
    with cls._lock:
      if not hasattr(cls, "instance"):
        cls.instance = super().__new__(cls)
        cls.instance.history = []
        cls.instance.future = []
    return cls.instance

  @thread_lock()
  def add_state(self, value: str):
    """Adds a new application state and removes future states."""
    self.history.append(value)
    self.future.clear()

  @thread_lock()
  def undo(self):
    """Removes the most recent application state and puts it into future."""
    sleep(1)
    if self.history:
      self.future.append(self.history.pop())

  @thread_lock()
  def redo(self):
    """Adds the most recently removed state as the most recent application state."""
    if self.future:
      self.history.append(self.future.pop())

  @thread_lock()
  def clear(self):
    self.history.clear()
    self.future.clear()

  @property
  def current_state(self):
    """Return the most recent application state."""
    return self.history[-1]
