import asyncssh
import asyncio
import logging
import contextlib
from rich.console import Console
from .session_tui import Tui

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

ANSI_CLEAR_SCREEN = "\x1b[2J"
ANSI_CURSOR_HOME = "\x1b[H"


class SSHChannelWriter:
    """Wrap an asyncssh channel to make it look like a file for Rich."""

    def __init__(self, chan):
        self._chan = chan

    def write(self, data):
        try:
            logger.debug(f"[SSH WRITE] len={len(data)} repr={repr(data[:50])}...")
            self._chan.write(data)
        except (BrokenPipeError, asyncio.CancelledError):
            pass

    def flush(self):
        pass


class MySSHServerSession(asyncssh.SSHServerSession):
    def connection_made(self, chan: asyncssh.SSHServerChannel):
        self._chan = chan
        self.running = True

    def connection_lost(self, exc):
        self.running = False
        if hasattr(self, "_tui_task"):
            self._tui_task.cancel()

    def pty_requested(self, term_type, term_size, term_modes):
        return True

    def shell_requested(self) -> bool:
        return True

    def session_started(self) -> None:
        self._width, self._height, _, _ = self._chan.get_terminal_size()
        logger.debug(f"[SSH] Session started: {self._width}x{self._height}")

        self._tui = Tui(self._width, self._height)
        self.console = Console(
            file=SSHChannelWriter(self._chan),
            force_terminal=True,
            color_system="truecolor",
            legacy_windows=False,
            width=self._width,
            height=self._height,
        )

        self.loop = asyncio.get_running_loop()
        self._resize_event = asyncio.Event()
        self._chan.set_line_mode(False)

        self._tui_task = asyncio.create_task(self.run_tui())
        self.running = True

    async def run_tui(self):
        logger.debug("run_tui() starting")
        try:
            self.redraw_tui()
            while self.running:
                if self._resize_event.is_set():
                    self._resize_event.clear()
                    self._tui.resize(self._width, self._height)
                    self.redraw_tui()
                    logger.debug(f"[TUI] Resized to {self._width}x{self._height}")

                await asyncio.sleep(0.1)

        except asyncio.CancelledError:
            logger.debug("run_tui() cancelled")
            pass

        except Exception as e:
            logger.exception(f"TUI loop exception: {e}")

        finally:
            if not self._chan.is_closing():
                self._chan.exit(0)

    def redraw_tui(self):
        """Clear the screen and redraw the TUI."""
        try:
            self.console.file.write(ANSI_CLEAR_SCREEN + ANSI_CURSOR_HOME)
            self.console.print(self._tui.renderable())
            self.console.file.flush()
        except Exception as e:
            logger.exception(f"Error during TUI redraw: {e}")

    def data_received(self, data, datatype):
        logger.debug(f"[SSH] Data received: {repr(data)}")
        if data and data.strip() == "q":
            asyncio.create_task(self._shutdown())

    async def _shutdown(self):
        logger.debug("[SSH] Shutting down session")
        self.running = False
        if hasattr(self, "_tui_task"):
            self._tui_task.cancel()
            with contextlib.suppress(asyncio.CancelledError):
                await self._tui_task
        if not self._chan.is_closing():
            self._chan.exit(0)

    def terminal_size_changed(self, width, height, pixwidth, pixheight) -> bool:
        logger.debug(f"[SSH] Terminal size changed: {width}x{height}")
        self._width = width
        self._height = height
        self.loop.call_soon_threadsafe(self._resize_event.set)
        return True
