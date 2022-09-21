from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Generator


class TextFile:
  source: Path
  text: Generator[str, None, None]

  def __init__(self, path: Path):
    self.source = path
    self.text = self.text_generator()

  def text_generator(self):
    """Generator that yields a line of text from the source."""
    with open(self.source, "r", encoding="UTF-8") as file:
      for line in file:
        yield line


class Reader:
  file: TextFile
  read_strategy: ReadStrategy
  strategies: dict[str, ReadStrategy]

  def __init__(self, file: TextFile):
    self.file = file
    self.strategies = {}

  def read(self):
    """Reads the text or changes strategy prior to reading text."""
    user_input = input()
    if user_input in self.strategies:
      self.change_strategy(user_input)
    else:
      return self.read_strategy.read(self.file.text_generator())

  def set_strategy(self, key: str, read_strategy: ReadStrategy):
    """Adds strategy to the strategies dictionary."""
    self.strategies[key] = read_strategy

  def change_strategy(self, key: str):
    """Changes the strategy to read text."""
    self.read_strategy = self.strategies[key]


class ReadStrategy(ABC):
  """The strategy for printing text output."""

  @abstractmethod
  def read(self, text: Generator[str, None, None]):
    """Algorithm to read text."""


class ReadSingleLine(ReadStrategy):
  """Reads a single line at a time."""

  def read(self, text: Generator[str, None, None]):
    """Read a single line with each input."""
    while True:
      try:
        print(next(text), end="")
        user_input = input()
        if user_input == "Esc":
          break
      except StopIteration:
        return


class ReadParagraph(ReadStrategy):
  """Reads one paragraph at a time."""

  def read(self, text: Generator[str, None, None]):
    """Reads lines until the current line is an empty new line ("\n") with each input."""
    while True:
      try:
        line = next(text)

        if line == "\n":
          user_input = input()

          if user_input == "Esc":
            break

        print(line, end="")

      except StopIteration:
        return


class ReadAll(ReadStrategy):
  """Reads the entire text at once."""

  def read(self, text: Generator[str, None, None]):
    """Reads lines until all lines are exhausted."""
    while True:
      try:
        print(next(text), end="")

      except StopIteration:
        return


@dataclass
class AutoRead(ReadStrategy):
  """Reads a single line at a specified interval."""
  interval: float

  def read(self, text: Generator[str, None, None]):
    """Reads lines until all lines are exhausted, with a delay between each line."""
    while True:
      try:
        print(next(text), end="")
        sleep(self.interval)
      except StopIteration:
        return
