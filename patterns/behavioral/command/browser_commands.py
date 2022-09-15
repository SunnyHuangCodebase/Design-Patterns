from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum


class Key(str, Enum):
  """Keyboard keys."""
  T = "T"
  TAB = "Tab"
  W = "W"
  F4 = "F4"


class Modifier(str, Enum):
  """Key modifiers"""
  CTRL = "Ctrl+"
  ALT = "Alt+"
  SHIFT = "Shift+"
  CTRLSHIFT = "Ctrl+Shift+"


@dataclass
class Hotkey:
  key: Key
  command: BrowserCommand
  modifier: Modifier | str = field(default_factory=str)

  def __str__(self):
    return f"{self.modifier}{self.key}"


@dataclass
class KeyPress:
  key: Key
  modifier: Modifier | str = field(default_factory=str)

  def __str__(self):
    return f"{self.modifier}{self.key}"


@dataclass
class Keyboard:
  computer: Computer

  def press_key(self, keypress: KeyPress):
    return self.computer.send_keypress(f"{keypress}")


@dataclass
class Computer:
  keyboard: Keyboard
  browser: WebBrowser
  active_window: App

  def __init__(self, browser: WebBrowser):
    self.keyboard = Keyboard(self)
    self.browser = browser
    self.set_active_window(self.browser)

  def set_active_window(self, app: App):
    self.active_window = app

  def send_keypress(self, key: str):
    return self.active_window.receive_keypress(key)


class App(ABC):
  """A computer application"""
  hotkeys: dict[str, BrowserCommand]

  def add_hotkey(self, hotkey: Hotkey):
    """Link Hotkey to a specific App Command."""
    self.hotkeys[f"{hotkey}"] = hotkey.command

  def receive_keypress(self, key: str):
    """Receives keyboard input."""

    if key in self.hotkeys:
      return self.hotkeys[key].execute()

    return key


class WebBrowser(App):
  """An app to view webpages."""
  tabs: list[str]
  closed_tabs: list[str]
  active_tab_index: int
  keyboard: Keyboard

  def __init__(self, tabs: list[str] | None = None):
    self.tabs = tabs or ["google.com"]
    self.closed_tabs = []
    self.active_tab_index = 0
    self.hotkeys = {}

  def next_tab_index(self):
    """Changes to the next tab index."""
    self.active_tab_index += 1

    if not self.active_tab_index in range(len(self.tabs)):
      self.active_tab_index = 0

  def prev_tab_index(self):
    """Changes to the next tab index."""
    self.active_tab_index -= 1

    if not self.active_tab_index in range(len(self.tabs)):
      self.active_tab_index = len(self.tabs) - 1

  def current_tab(self):
    """Returns the current tab."""
    return self.tabs[self.active_tab_index]


class BrowserCommand(ABC):
  """Web Browser commands."""

  @abstractmethod
  def execute(self) -> str:
    """Executes a command."""


@dataclass
class NewTab(BrowserCommand):
  """Open new browser tab."""
  browser: WebBrowser

  def execute(self) -> str:
    self.browser.tabs.append("New Tab")
    self.browser.next_tab_index()
    return self.browser.current_tab()


@dataclass
class CycleTab(BrowserCommand):
  """Cycles through open browser tabs."""
  browser: WebBrowser

  def execute(self) -> str:
    """Goes through the tab list."""
    self.browser.next_tab_index()
    return self.browser.current_tab()


@dataclass
class ReverseCycleTab(BrowserCommand):
  """Cycles through open browser tabs."""
  browser: WebBrowser

  def execute(self) -> str:
    """Goes through the tab list."""
    self.browser.prev_tab_index()
    return self.browser.current_tab()


@dataclass
class CloseTab(BrowserCommand):
  """Closes current browser tab."""
  browser: WebBrowser

  def execute(self) -> str:
    """Removes current tab from tabs and adds it to closed tabs."""
    tab = self.browser.current_tab()
    self.browser.tabs.remove(tab)
    self.browser.prev_tab_index()
    self.browser.closed_tabs.append(tab)
    return self.browser.current_tab()


@dataclass
class UndoCloseTab(BrowserCommand):
  """Reopen last closed browser tab."""
  browser: WebBrowser

  def execute(self) -> str:
    """Reopens the last closed tab and activates it."""
    if not self.browser.closed_tabs:
      return ""

    self.browser.active_tab_index = len(self.browser.tabs)
    self.browser.tabs.append(self.browser.closed_tabs.pop())
    return self.browser.current_tab()
