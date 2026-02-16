import contextlib
from asyncssh import SSHServerChannel

class SSHChannelWriter:
    """Wrap an asyncssh channel and provide helper methods for terminal actions."""

    def __init__(self, chan: SSHServerChannel):
        self._chan = chan

    def write(self, data: str):
        """File-like interface for Rich; do nothing."""
        pass

    def flush(self):
        """File-like interface for Rich; do nothing."""
        pass

    # --- Terminal control helpers ---
    def write_tui(self, text: str):
        """Write rendered TUI text to the channel."""
        self._chan.write(text)

    def set_cursor_visibility(self, visible: bool):
        """Show or hide the cursor."""
        self._chan.write(f"\x1b[?25{'h' if visible else 'l'}")

    def set_alt_screen(self, enable: bool):
        """Enable or disable alternate screen buffer."""
        self._chan.write(f"\x1b[?1049{'h' if enable else 'l'}")

    def clear_screen(self):
        """Clear screen and move cursor to home."""
        self._chan.write("\x1b[2J\x1b[H")

    def set_window_title(self, title: str):
        """Set the terminal window title."""
        self._chan.write(f"\x1b]0;{title}\x07")

    def clear_input(self):
        """Disable/clear input line."""
        with contextlib.suppress(Exception):
            self._chan.clear_input()

    def set_line_mode(self, enabled: bool):
        """Set line mode on the SSH channel."""
        with contextlib.suppress(Exception):
            self._chan.set_line_mode(enabled)

    def set_echo(self, enabled: bool):
        """Enable/disable echo on the SSH channel."""
        with contextlib.suppress(Exception):
            self._chan.set_echo(enabled)

