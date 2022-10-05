"""The Task App implements the Memento  design pattern.

The TaskApp may contain a history of states to enable undo/redo functionality.
It can create TaskStates whenever it performs a new action.
These TaskStates can then be added to a list of TaskStates in a TaskHistory.
TaskHistory is responsible for rolling back changes or reverting undo actions.

Each component of the Memento pattern has one job.
The TaskApp keeps track of tasks and is the Originator of TaskStates.
TaskStates serve as the Memento, which contains the internal state of the TaskApp.
TaskHistory is the Caretaker, managing TaskApp's state via undo/redo functions.
"""

from __future__ import annotations
from dataclasses import dataclass, field


class TaskApp:
  """App to manage daily tasks.
  The 'Originator' in the Memento Design Pattern."""
  _to_do_list: dict[int, str]
  _completed_tasks: dict[int, str]
  _last_task_id: int

  def __init__(self) -> None:
    self._to_do_list = {}
    self._completed_tasks = {}
    self._last_task_id = 0

  def add_task(self, task: str):
    """Adds a task to the task list."""
    task_id = self.next_task_id()
    self._to_do_list[task_id] = task

  def next_task_id(self) -> int:
    """Increments the last task ID number and returns it."""
    self._last_task_id += 1
    return self._last_task_id

  def remove_task(self, id: int):
    """Removes the task from the task list"""
    del self._to_do_list[id]

  def complete_task(self, id: int):
    """Moves a task from the task list to the completed list."""
    task = self._to_do_list[id]
    del self._to_do_list[id]
    self._completed_tasks[id] = task

  def current_state(self) -> TaskState:
    """Saves the app state as a memento."""
    return TaskState(
        self._to_do_list.copy(),
        self._completed_tasks.copy(),
        self._last_task_id,
    )

  def restore_state(self, memento: TaskState):
    """Restores the state from memento."""
    self._to_do_list = memento.to_do_list.copy()
    self._completed_tasks = memento.completed_tasks.copy()
    self._last_task_id = memento.last_task_id


@dataclass
class TaskState:
  """Stores the app state before every action.
  The 'Memento' in the Memento Design Pattern."""
  to_do_list: dict[int, str]
  completed_tasks: dict[int, str]
  last_task_id: int


@dataclass
class TaskHistory:
  """Manages the state of the task app.
  The 'Caretaker' in the Memento Design Pattern."""
  _app: TaskApp
  _history: list[TaskState] = field(default_factory=list)
  _undo_history: list[TaskState] = field(default_factory=list)

  def backup(self):
    """Adds a memento to _history."""
    self._history.append(self._app.current_state())
    self._undo_history.clear()

  def undo(self):
    """Reverts to the previous state, if any."""
    state = self._history.pop()

    if not self._history:
      self._history.append(state)

    if self._app.current_state() != state:
      self._undo_history.append(self._app.current_state())
      self._app.restore_state(state)

  def redo(self):
    """Reverses an undo action, if any."""
    if not self._undo_history:
      return

    state = self._undo_history.pop()

    self._history.append(state)
    self._app.restore_state(state)

  @property
  def history(self) -> list[TaskState]:
    return self._history

  @property
  def undo_history(self) -> list[TaskState]:
    return self._undo_history
