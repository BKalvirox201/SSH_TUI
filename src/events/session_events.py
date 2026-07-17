from dataclasses import dataclass


# NOTE: ALL EVENTS ARE SESSION EVENTS
@dataclass
class SessionEvent:
    pass


@dataclass
class SessionClose(SessionEvent):
    exit_code: int  # TODO: Make it into a type
    exit_message: str


@dataclass
class ChangePage(SessionEvent):
    page_name: str


@dataclass
class Tick(SessionEvent):
    pass


@dataclass
class ChangeInputType(SessionEvent):
    pass
