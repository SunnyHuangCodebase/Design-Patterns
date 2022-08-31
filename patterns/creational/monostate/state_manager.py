from __future__ import annotations
from threading import Lock, Thread
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


if __name__ == "__main__":

  a = StateManager()
  b = StateManager()
  print(f"Are {a = } and {b = } equivalent? {a == b = }")
  print(
      f"Are {a.history = } and {b.history = } equivalent? {a.history is b.history = }"
  )
  a.add_state("Test 1")
  print(a.history, b.history)
  b.add_state("Test 2")
  print(a.history, b.history)
  a.undo()
  print(a.history, b.history)
  print(id(a.history))
  a.clear()
  print(id(a.__dict__))
  print(id(b.__dict__))

  def main():
    """Create two variables instantiating StateManager, but point to the same object."""
    app_x = StateManager()
    app_y = StateManager()
    app_x.add_state("Action 1")
    app_y.add_state("Action 2")

    # Monostate returns different instances of StateManager
    print(f"{(app_x == app_y) = }")

    app_y.undo()
    app_x.add_state("Action 3")

  main()
  app = StateManager()
  print(app.history)    # Returns ["State 1", "State 3"]

  # Reset app history
  app.clear()

  def add_app_state(value: str, lock: Lock):
    with lock:
      app = StateManager()
      app.add_state(value)

      # Without thread lock on undo method, this deletes most recent state and not "State 2"
      if value == "State 2":
        sleep(1)
        app.undo()

      # app variable will return a separate instance of app.
      print(app)
      # However, its __dict__ is the same each time
      print("a", app.__dict__)
      print(id(app.history))
      print(app.history)

  lock = Lock()

  def main2():
    """Runs multiple locked threads that call the Singleton"""
    thread1 = Thread(target=add_app_state, args=("State 1", lock))
    thread2 = Thread(target=add_app_state, args=("State 2", lock))
    thread3 = Thread(target=add_app_state, args=("State 3", lock))
    thread4 = Thread(target=add_app_state, args=("State 4", lock))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

  main2()

  app = StateManager()
  # Without thread lock on the Thread target, this returns ["Action 1, Action 2"]
  print(app.history)    # Returns ["Action 1", "Action 3"]
