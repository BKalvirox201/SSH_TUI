import asyncio
from enum import Enum, auto
import logging

from src.events.global_events import InputEvent


class InputMode(Enum):
    KEY_BY_KEY = auto()
    LINE = auto()


class InputHandler:
    """Handles raw input and converts it to events according to the current input mode."""

    def __init__(self, event_queue: asyncio.Queue, logger: logging.LoggerAdapter):
        self.event_queue = event_queue
        self.logger = logger
        self.input_mode = InputMode.KEY_BY_KEY
        self.line_buffer = ""

    def set_mode(self, mode: InputMode):
        """Switch between key-by-key and line modes."""
        self.input_mode = mode
        if mode == InputMode.LINE:
            self.line_buffer = ""

    def handle_input(self, data: str):
        """Process incoming raw data and enqueue events."""
        self.logger.debug(f"[InputHandler] Data received: {data!r}")

        if self.input_mode == InputMode.KEY_BY_KEY:
            for char in data:
                if char.strip():
                    self.event_queue.put_nowait(InputEvent(char))

        elif self.input_mode == InputMode.LINE:
            self.line_buffer += data
            while "\n" in self.line_buffer:
                line, remainder = self.line_buffer.split("\n", 1)
                self.line_buffer = remainder
                self.event_queue.put_nowait(InputEvent(line.strip()))
