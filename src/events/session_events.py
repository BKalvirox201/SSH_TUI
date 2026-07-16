from dataclasses import dataclass


@dataclass
class SessionEvent:
    pass


@dataclass
class SessionClose(SessionEvent):
    exit_code: int  # TODO: Make it into a type
    exit_message: str


@dataclass
class ChangeCurrentPage(SessionEvent):
    new_page_name: str


@dataclass
class Tick(SessionEvent):
    pass


@dataclass
class ChangeInputType(SessionEvent):
    pass
