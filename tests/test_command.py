import pytest

from patterns.behavioral.command.browser_commands import CloseTab, Computer, CycleTab, Hotkey, Key, KeyPress, Modifier, NewTab, ReverseCycleTab, UndoCloseTab, WebBrowser


class TestCommand:

  @pytest.fixture
  def browser(self):
    browser = WebBrowser()

    hotkeys = [
        Hotkey(Key.T, NewTab(browser), Modifier.CTRL),
        Hotkey(Key.TAB, CycleTab(browser), Modifier.CTRL),
        Hotkey(Key.TAB, ReverseCycleTab(browser), Modifier.CTRLSHIFT),
        Hotkey(Key.W, CloseTab(browser), Modifier.CTRL),
        Hotkey(Key.F4, CloseTab(browser), Modifier.CTRL),
        Hotkey(Key.T, UndoCloseTab(browser), Modifier.CTRLSHIFT),
    ]

    for hotkey in hotkeys:
      browser.add_hotkey(hotkey)

    return browser

  @pytest.fixture
  def pc(self, browser: WebBrowser):
    return Computer(browser)

  def test_commands(self, pc: Computer):
    assert pc.keyboard.press_key(KeyPress(Key.T)) == "T"
    assert pc.keyboard.press_key(KeyPress(Key.T, Modifier.CTRLSHIFT)) == ""
    assert pc.keyboard.press_key(KeyPress(Key.TAB,
                                          Modifier.CTRL)) == "google.com"
    assert pc.keyboard.press_key(KeyPress(Key.TAB,
                                          Modifier.CTRLSHIFT)) == "google.com"
    assert pc.keyboard.press_key(KeyPress(Key.T, Modifier.CTRL)) == "New Tab"
    pc.keyboard.press_key(KeyPress(Key.T, Modifier.CTRL))
    assert pc.keyboard.press_key(KeyPress(Key.F4, Modifier.CTRL)) == "New Tab"
    assert pc.keyboard.press_key(KeyPress(Key.W, Modifier.CTRL)) == "google.com"
    assert pc.keyboard.press_key(KeyPress(Key.T,
                                          Modifier.CTRLSHIFT)) == "New Tab"


if __name__ == "__main__":
  pytest.main([__file__])
