import asyncssh
import asyncio
import logging
import contextlib
from typing import cast
from rich.console import Console
from ..tui.tui import Tui

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

ESC = "\x1b"
BEL = "\x07"


def show_cursor() -> str:
    """Show the terminal cursor."""
    return f"{ESC}[?25h"


def hide_cursor() -> str:
    """Hide the terminal cursor."""
    return f"{ESC}[?25l"


def set_alt_screen(enable: bool) -> str:
    """Enable or disable the alternate screen buffer."""
    return f"{ESC}[?1049{'h' if enable else 'l'}"


def clear_screen() -> str:
    """Clear entire screen and move cursor to home."""
    return f"{ESC}[2J{ESC}[H"


def set_window_title(title: str) -> str:
    """Set terminal window title."""
    return f"{ESC}]0;{title}{BEL}"


class SSHChannelWriter:
    """Wrap an asyncssh channel to make it look like a file for Rich."""

    def __init__(self, chan):
        self._chan = chan

    def write(self, data: str):
        pass
        #self._chan.write(data) # remove final /r/n

    def flush(self):
        pass


class MySSHServerSession(asyncssh.SSHServerSession):
    def connection_made(self, chan: asyncssh.SSHServerChannel):
        self._chan = cast(asyncssh.SSHLineEditorChannel, chan)

    def connection_lost(self, exc):
        asyncio.create_task(self._shutdown())

    def pty_requested(self, term_type, term_size, term_modes):
        self._width, self._height, _, _ = term_size
        return True

    def shell_requested(self) -> bool:
        return True

    def session_started(self) -> None:
        try:
            self._chan.clear_input()
            self._chan.set_line_mode(False)
            self._chan.set_echo(False)
            self._tui = Tui(self._width, self._height)
            self.console = Console(
                file=SSHChannelWriter(self._chan),
                force_terminal=True,
                color_system="truecolor",
                record=True,
                width=self._width,
                height=self._height,
            )

            self.loop = asyncio.get_running_loop()
            self._resize_event = asyncio.Event()
            self._chan.write(set_alt_screen(True))
            self._chan.write(set_window_title("MyWindowTitle"))
            self._chan.write(hide_cursor())
            self.running = True
            self.draw_tui()
            self._tui_task = asyncio.create_task(self.run_tui())

        except Exception as e:
            logger.error(f"Session started exception: {e}")

    async def run_tui(self):
        try:
            while self.running:
                if self._resize_event.is_set():
                    self._resize_event.clear()
                    self._tui.resize(self._width, self._height)
                    self.draw_tui()
                await asyncio.sleep(0.01)

        except asyncio.CancelledError:
            pass

        except Exception as e:
            logger.exception(f"TUI loop exception: {e}")

    def draw_tui(self):
        try:
            self._chan.write(clear_screen())
            self.console.print(self._tui.render(), soft_wrap=False, end="")
            recorded_tui = self.console.export_text(clear=True, styles=True)[:-2]
            self._chan.write(recorded_tui)
            # logger.info(repr(recorded_tui))
        except Exception as e:
            logger.exception(f"Error during TUI redraw: {e}")

    def data_received(self, data: str, datatype):
        logger.debug(f"[SSH] Data received: {repr(data)}")
        if data and data.strip() in ('q', '\x03'):
            asyncio.create_task(self._shutdown())

    async def _shutdown(self):
        if not getattr(self, "running", False):
            return

        self.running = False
        if hasattr(self, "_tui_task"):
            self._tui_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._tui_task

        if hasattr(self, "console"):
            try:
                self._chan.write(show_cursor())
                self._chan.write(set_alt_screen(False))
            except Exception as e:
                logger.exception(f"_shutdown: failed to restore cursor: {e}")

        if hasattr(self, "_chan") and not self._chan.is_closing():
            self._chan.exit(0)

    def terminal_size_changed(self, width, height, pixwidth, pixheight):
        self._width = width
        self._height = height
        if hasattr(self, "console") and self.console is not None:
            self.console.width = self._width
            self.console.height = self._height
        if hasattr(self, "_tui"):
            self._tui.resize(width, height)
        if hasattr(self, "_resize_event"):
            self._resize_event.set()
        return True
