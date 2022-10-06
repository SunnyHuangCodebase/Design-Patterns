import pytest

from patterns.behavioral.command.browser_commands import BrowserController, CloseAllTabs, CloseTab, CompositeBrowserCommand, CycleTab, Key, KeyCombination, Modifier, NewTab, ReverseCycleTab, TabHistory, UndoCloseTab, WebBrowser


class TestCommand:

  @pytest.fixture
  def browser(self) -> WebBrowser:
    browser = WebBrowser()

    return browser

  @pytest.fixture
  def controller(self, browser: WebBrowser) -> BrowserController:
    controller = BrowserController()

    reset_browser = CompositeBrowserCommand(browser)
    reset_browser.add(CloseAllTabs(browser))
    reset_browser.add(NewTab(browser))

    history = TabHistory()
    close_tab = CloseTab(browser, history)
    undo_close_tab = UndoCloseTab(browser, history)

    shortcuts = [
        (KeyCombination(Key.T, Modifier.CTRL), NewTab(browser)),
        (KeyCombination(Key.TAB, Modifier.CTRL), CycleTab(browser)),
        (KeyCombination(Key.TAB, Modifier.CTRLSHIFT), ReverseCycleTab(browser)),
        (KeyCombination(Key.W, Modifier.CTRL), close_tab),
        (KeyCombination(Key.F4, Modifier.CTRL), close_tab),
        (KeyCombination(Key.T, Modifier.CTRLSHIFT), undo_close_tab),
        (KeyCombination(Key.W, Modifier.CTRLSHIFT), CloseAllTabs(browser)),
        (KeyCombination(Key.R, Modifier.CTRLSHIFT), reset_browser),
    ]

    for hotkey, command in shortcuts:
      controller.register_hotkey(hotkey, command)

    return controller

  def test_new_browser(self, browser: WebBrowser):
    assert browser.tabs == ["google.com"]

  def test_regular_keystroke(self, browser: WebBrowser,
                             controller: BrowserController):
    assert controller.send_keystrokes(KeyCombination(Key.T)) == "T"
    assert controller.send_keystrokes(KeyCombination(Key.T,
                                                     Modifier.ALT)) == "T"
    assert browser.tabs == ["google.com"]

  def test_no_closed_tabs(self, browser: WebBrowser,
                          controller: BrowserController):
    controller.send_keystrokes(KeyCombination(Key.T, Modifier.CTRLSHIFT))
    assert browser.tabs == ["google.com"]

  def test_cycle_through_tabs(self, browser: WebBrowser,
                              controller: BrowserController):

    controller.send_keystrokes(KeyCombination(Key.TAB, Modifier.CTRL))
    assert browser.current_tab() == "google.com"
    controller.send_keystrokes(KeyCombination(Key.TAB, Modifier.CTRL))
    assert browser.current_tab() == "google.com"
    controller.send_keystrokes(KeyCombination(Key.TAB, Modifier.CTRLSHIFT))
    controller.send_keystrokes(KeyCombination(Key.TAB, Modifier.CTRLSHIFT))
    controller.send_keystrokes(KeyCombination(Key.TAB, Modifier.CTRLSHIFT))
    assert browser.current_tab() == "google.com"

  def test_new_tab(self, browser: WebBrowser, controller: BrowserController):

    controller.send_keystrokes(KeyCombination(Key.T, Modifier.CTRL))
    assert browser.current_tab() == "New Tab"

  def test_close_tab(self, browser: WebBrowser, controller: BrowserController):
    controller.send_keystrokes(KeyCombination(Key.T, Modifier.CTRL))
    controller.send_keystrokes(KeyCombination(Key.T, Modifier.CTRL))
    assert browser.current_tab() == "New Tab"

    controller.send_keystrokes(KeyCombination(Key.F4, Modifier.CTRL))
    assert browser.current_tab() == "New Tab"

    controller.send_keystrokes(KeyCombination(Key.W, Modifier.CTRL))
    assert browser.current_tab() == "google.com"

    controller.send_keystrokes(KeyCombination(Key.T, Modifier.CTRLSHIFT))
    assert browser.current_tab() == "New Tab"

  def test_close_all_tabs(self, browser: WebBrowser,
                          controller: BrowserController):
    controller.send_keystrokes(KeyCombination(Key.W, Modifier.CTRLSHIFT))
    assert browser.tabs == []

  def reset_browser(self, browser: WebBrowser, controller: BrowserController):
    controller.send_keystrokes(KeyCombination(Key.R, Modifier.CTRLSHIFT))
    assert browser.current_tab() == "New Tab"


if __name__ == "__main__":
  pytest.main([__file__, "-v"])
