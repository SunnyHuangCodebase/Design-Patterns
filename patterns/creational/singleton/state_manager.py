from __future__ import annotations
from threading import Lock, Thread
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


if __name__ == "__main__":

  def main():
    """Create two variables instantiating StateManager, but point to the same object."""
    app_x = StateManager()
    app_y = StateManager()
    app_x.add_state("Action 1")
    app_y.add_state("Action 2")

    #Singleton Returns the same object
    print(f"{(app_x == app_y) = }")

    # Thread locked undo method has a timer before executing logic.
    app_y.undo()

    # Without previous thread lock, undo removes "Action 3" instead of "Action 2".
    app_x.add_state("Action 3")

  main()
  app = StateManager()

  # Without thread lock on the Thread target, this returns ["Action 1, Action 2"]
  print(app.history)    # Returns ["Action 1", "Action 3"]

  # Reset app history
  app.clear()

  @thread_lock()
  def add_app_state(value: str):
    app = StateManager()
    app.add_state(value)

    # Without thread lock on undo method, this deletes most recent state and not "State 2"
    if value == "State 2":
      sleep(1)
      app.undo()

    # app variable always returns the same Singleton object.
    print(app)

  def main2():
    """Runs multiple locked threads that call the Singleton"""
    thread1 = Thread(target=add_app_state, args=("State 1",))
    thread2 = Thread(target=add_app_state, args=("State 2",))
    thread3 = Thread(target=add_app_state, args=("State 3",))
    thread4 = Thread(target=add_app_state, args=("State 4",))

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

  # Without thread locked undo method, this returns ["State 1, State 2"]
  print(app.history)    # Returns ["State 1", "State 3"]
