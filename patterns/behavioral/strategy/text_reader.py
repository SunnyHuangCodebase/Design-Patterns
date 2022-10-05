"""TextReader uses the Strategy design pattern to read a text file in many ways.
It uses composition to contain a text file and list of strategies.
In this way, it adheres to the Single Responsibility Principle.

Creating a new strategy involves subclassing ReadingStrategy (inheritance).
However, it is also possible to convert ReadingStrategy to a Protocol.
In this case, all variations of ReadingStrategy would follow the protocol (polymorphism) 
Then we can use dependency injection instead of composition to read a file.

Example:
  class ReadingStrategy(typing.Protocol):
    def read(self, file):
      ...
  
  class ReadSingleLine:
    def read(self, file):
      '''Read one line at a time'''
      pass
  
  class TextReader:
    file: TextFile

    def __init__(self, file_path: Path):
  
    def read(self, read_strategy: ReadingStrategy):
      read_strategy.read(self.file)
  file_path = Path.cwd() / "file.txt"
  reader = TextReader(file_path)
  reader.read(ReadSingleLine())

The Strategy design pattern focuses on how an object performs a task (algorithms).
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from time import sleep
from typing import Generator


class TextReader:
  """Contains a TextFile object and a list of strategies to read that text file.

  Each ReadStrategy offers a different way to read text, based on preference.
  It's also possible to change the strategy in the middle of reading the text.
  """
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


class TextFile:
  """Contains a file source and a generator with the file's text."""
  source: Path
  text: Generator[str, None, None]

  def __init__(self, path: Path):
    self.source = path
    self.text = self.text_generator()

  def text_generator(self):
    """Generator that yields a line of text from the source."""
    # with open(self.source, "r", encoding="UTF-8") as file:
    with self.source.open() as file:
      for line in file:
        yield line


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
