from pathlib import Path
import textwrap
from time import time
from typing import Callable
import pytest
from pytest import CaptureFixture, MonkeyPatch, TempPathFactory

from patterns.behavioral.strategy.text_reader import AutoRead, ReadAll, ReadParagraph, ReadSingleLine, TextReader, TextFile


class TestStrategy:

  @pytest.fixture(scope="module")
  def text(self) -> str:
    return textwrap.dedent("""\
      Paragraph 1 Line 1
      Paragraph 1 Line 2
      Paragraph 1 Line 3
      Paragraph 1 Line 4

      Paragraph 2 Line 1
      Paragraph 2 Line 2
      Paragraph 2 Line 3
      Paragraph 2 Line 4
      
      Paragraph 3 Line 1
      Paragraph 3 Line 2
      Paragraph 3 Line 3
      Paragraph 3 Line 4""")

  @pytest.fixture(scope="module")
  def path(self, text: str, tmp_path_factory: TempPathFactory) -> Path:
    path = tmp_path_factory.mktemp("data") / "file.txt"
    path.write_text(text, "UTF-8")
    return path

  @pytest.fixture(scope="module")
  def alternative_path(self, text: str, tmp_path: Path) -> Path:
    path = tmp_path / "data"
    path.mkdir()
    path /= "file.txt"
    path.write_text(text)
    return path

  @pytest.fixture(scope="module")
  def file(self, path: Path) -> TextFile:
    return TextFile(path)

  def test_read_single_line(self, file: TextFile, capsys: CaptureFixture[str],
                            monkeypatch: MonkeyPatch):
    inputs = ["1", "", "Esc"]
    next_input: Callable[..., str] = lambda: inputs.pop(0)
    monkeypatch.setattr("builtins.input", next_input)
    reader = TextReader(file)
    reader.set_strategy("1", ReadSingleLine())

    reader.read()
    reader.read()

    captured = capsys.readouterr()
    assert captured.out == textwrap.dedent("""\
      Paragraph 1 Line 1
      """)

  def test_read_entire_file_with_single_line_strategy(
      self, file: TextFile, capsys: CaptureFixture[str],
      monkeypatch: MonkeyPatch):

    monkeypatch.setattr("builtins.input", lambda: "")
    reader = TextReader(file)
    reader.set_strategy("1", ReadSingleLine())
    reader.change_strategy("1")
    reader.read()

    captured = capsys.readouterr()
    assert captured.out == textwrap.dedent("""\
      Paragraph 1 Line 1
      Paragraph 1 Line 2
      Paragraph 1 Line 3
      Paragraph 1 Line 4

      Paragraph 2 Line 1
      Paragraph 2 Line 2
      Paragraph 2 Line 3
      Paragraph 2 Line 4
      
      Paragraph 3 Line 1
      Paragraph 3 Line 2
      Paragraph 3 Line 3
      Paragraph 3 Line 4""")

  def test_read_entire_file_with_paragraph_strategy(self, file: TextFile,
                                                    capsys: CaptureFixture[str],
                                                    monkeypatch: MonkeyPatch):
    monkeypatch.setattr("builtins.input", lambda: "")
    reader = TextReader(file)
    reader.set_strategy("1", ReadParagraph())
    reader.change_strategy("1")
    reader.read()

    captured = capsys.readouterr()
    assert captured.out == textwrap.dedent("""\
      Paragraph 1 Line 1
      Paragraph 1 Line 2
      Paragraph 1 Line 3
      Paragraph 1 Line 4

      Paragraph 2 Line 1
      Paragraph 2 Line 2
      Paragraph 2 Line 3
      Paragraph 2 Line 4
      
      Paragraph 3 Line 1
      Paragraph 3 Line 2
      Paragraph 3 Line 3
      Paragraph 3 Line 4""")

  def test_read_paragraph(self, file: TextFile, capsys: CaptureFixture[str],
                          monkeypatch: MonkeyPatch):
    inputs = ["", "", "Esc"]
    next_input: Callable[..., str] = lambda: inputs.pop(0)
    monkeypatch.setattr("builtins.input", next_input)
    reader = TextReader(file)
    reader.set_strategy("1", ReadParagraph())
    reader.change_strategy("1")
    reader.read()

    captured = capsys.readouterr()
    assert captured.out == textwrap.dedent("""\
      Paragraph 1 Line 1
      Paragraph 1 Line 2
      Paragraph 1 Line 3
      Paragraph 1 Line 4

      Paragraph 2 Line 1
      Paragraph 2 Line 2
      Paragraph 2 Line 3
      Paragraph 2 Line 4
      """)

  def test_read_all(self, file: TextFile, capsys: CaptureFixture[str],
                    monkeypatch: MonkeyPatch):

    monkeypatch.setattr("builtins.input", lambda: "")
    reader = TextReader(file)
    reader.set_strategy("1", ReadAll())
    reader.change_strategy("1")
    reader.read()

    captured = capsys.readouterr()
    assert captured.out == textwrap.dedent("""\
      Paragraph 1 Line 1
      Paragraph 1 Line 2
      Paragraph 1 Line 3
      Paragraph 1 Line 4

      Paragraph 2 Line 1
      Paragraph 2 Line 2
      Paragraph 2 Line 3
      Paragraph 2 Line 4
      
      Paragraph 3 Line 1
      Paragraph 3 Line 2
      Paragraph 3 Line 3
      Paragraph 3 Line 4""")

  def test_auto_read(self, file: TextFile, capsys: CaptureFixture[str],
                     monkeypatch: MonkeyPatch):
    inputs = ["", "", "Esc"]
    next_input: Callable[..., str] = lambda: inputs.pop(0)
    monkeypatch.setattr("builtins.input", next_input)
    reader = TextReader(file)
    interval = 0.2
    reader.set_strategy("1", AutoRead(interval))
    reader.change_strategy("1")
    start = time()
    reader.read()
    time_elapsed = time() - start
    captured = capsys.readouterr()

    assert time_elapsed >= captured.out.count("\n") * interval
    assert captured.out == textwrap.dedent("""\
      Paragraph 1 Line 1
      Paragraph 1 Line 2
      Paragraph 1 Line 3
      Paragraph 1 Line 4

      Paragraph 2 Line 1
      Paragraph 2 Line 2
      Paragraph 2 Line 3
      Paragraph 2 Line 4
      
      Paragraph 3 Line 1
      Paragraph 3 Line 2
      Paragraph 3 Line 3
      Paragraph 3 Line 4""")


if __name__ == "__main__":
  pytest.main([__file__])
