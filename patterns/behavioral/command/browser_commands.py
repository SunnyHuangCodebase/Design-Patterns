"""The Browser Command module uses the Command design pattern to send commands.

The Sender never interacts directly with the Receiver, but with a Command Interface.
A concrete Command then delegates the work to the Receiver.

As a result, the Sender and Receiver are loosely coupled.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class Key(str, Enum):
  """Keyboard keys."""
  R = "R"
  T = "T"
  TAB = "Tab"
  W = "W"
  F4 = "F4"


class Modifier(str, Enum):
  """Key modifiers"""
  CTRL = "Ctrl+"
  ALT = "Alt+"
  CTRLSHIFT = "Ctrl+Shift+"


@dataclass
class KeyCombination:
  """Key combinations."""
  key: Key
  modifier: Modifier | str = field(default_factory=str)

  @property
  def value(self) -> str:
    return f"{self.modifier}+{self.key}"


class Command(Protocol):
  """Command that is sent from a Sender to Receiver."""

  def execute(self) -> Any:
    """Instructs the Receiver to executes a command."""


class BrowserController:
  """Controls the browser with commands."""
  commands: dict[str, BrowserCommand]

  def __init__(self):
    self.commands = {}

  def register_hotkey(self, key_combination: KeyCombination,
                      command: BrowserCommand):
    """Associates a hotkey to a command."""
    self.commands[key_combination.value] = command

  def send_keystrokes(self, key_combination: KeyCombination) -> str | None:
    """Searches for the keystroke in commands, then executes the command, if any.
    Otherwise, returns the key pressed."""
    command = self.commands.get(key_combination.value, None)

    if command:
      return command.execute()

    else:
      return key_combination.key.value


class WebBrowser:
  """An app to view webpages."""
  tabs: list[str]
  active_tab_index: int

  def __init__(self, tabs: list[str] | None = None):
    self.tabs = tabs or ["google.com"]
    self.active_tab_index = 0

  def next_tab_index(self):
    """Changes to the next tab index."""
    self.active_tab_index += 1

    if self.active_tab_index not in range(len(self.tabs)):
      self.active_tab_index = 0

  def prev_tab_index(self):
    """Changes to the next tab index."""
    self.active_tab_index -= 1

    if not self.active_tab_index in range(len(self.tabs)):
      self.active_tab_index = len(self.tabs) - 1

  def current_tab(self):
    """Returns the current tab."""
    return self.tabs[self.active_tab_index]

  def new_tab(self, tab: str = "New Tab"):
    """Opens a new tab."""
    self.tabs.append(tab)
    self.active_tab_index = len(self.tabs) - 1

  def cycle_tab(self, /, *, reverse: bool = False):
    """Cycles through tab list in order or reverse order."""
    if not reverse:
      self.next_tab_index()
    else:
      self.prev_tab_index()

  def close_current_tab(self) -> str:
    """Removes current tab from tabs and adds it to closed tabs."""
    tab = self.current_tab()
    self.tabs.remove(tab)
    self.prev_tab_index()
    return tab

  def close_all_tabs(self):
    """Close all tabs and add it to closed tabs."""
    while self.tabs:
      self.close_current_tab()


class BrowserCommand(ABC):
  """Web Browser commands."""
  app: WebBrowser

  def __init__(self, app: WebBrowser) -> None:
    self.app = app

  @abstractmethod
  def execute(self) -> str | None:
    """Executes a browser command."""


class NewTab(BrowserCommand):
  """Open new browser tab."""

  def execute(self) -> None:
    """Opens a new tab."""
    self.app.new_tab()


class CycleTab(BrowserCommand):
  """Cycles through open browser tabs."""

  def execute(self) -> None:
    """Cycle through the tab list in order."""
    self.app.cycle_tab()


class ReverseCycleTab(BrowserCommand):
  """Cycles through open browser tabs."""

  def execute(self) -> None:
    """Cycle through the tab list in reverse order."""
    self.app.cycle_tab(reverse=True)


class CloseAllTabs(BrowserCommand):
  """Close all open tabs."""

  def execute(self) -> None:
    """Close tabs."""
    self.app.close_all_tabs()


@dataclass
class CompositeBrowserCommand(BrowserCommand):
  """A batch of browser commands."""
  app: WebBrowser
  commands: list[BrowserCommand] = field(default_factory=list)

  def add(self, command: BrowserCommand) -> None:
    """Adds a command to the batch of commands."""
    self.commands.append(command)

  def execute(self) -> None:
    """Executes all commands."""
    for command in self.commands:
      command.execute()


class ReversibleTabCommand(BrowserCommand, ABC):
  """Allows undo browser command."""
  app: WebBrowser
  history: TabHistory
  closed_tab: str

  def __init__(self, app: WebBrowser, history: TabHistory):
    self.app = app
    self.history = history


class UndoBrowserCommand(BrowserCommand, ABC):
  """Undo a reversible browser command"""
  app: WebBrowser
  history: TabHistory
  closed_tab: str

  def __init__(self, app: WebBrowser, history: TabHistory):
    self.app = app
    self.history = history


class CloseTab(ReversibleTabCommand):
  """Closes current browser tab."""
  app: WebBrowser
  history: TabHistory
  closed_tab: str

  def execute(self) -> None:
    """Closes the current tab."""
    self.closed_tab = self.app.close_current_tab()
    self.history.push(self)


class UndoCloseTab(UndoBrowserCommand):
  """Reopen last closed browser tab."""

  def execute(self) -> None:
    """Opens the last closed tab."""
    try:
      last_command = self.history.pop()
      self.app.new_tab(last_command.closed_tab)
    except IndexError:
      pass


@dataclass
class TabHistory:
  history: list[ReversibleTabCommand] = field(default_factory=list)

  def push(self, command: ReversibleTabCommand):
    """Pushes a command to the end of history."""
    self.history.append(command)

  def pop(self):
    """Pops the last command in history."""
    return self.history.pop()
