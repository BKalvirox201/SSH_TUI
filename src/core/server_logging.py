from datetime import datetime
import logging


class SessionFormatter(logging.Formatter):
    def format(self, record):
        session_id = getattr(record, "session_id", "unknown")
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{session_id}: {time_str}: {record.levelname}: {record.getMessage()}"


# Session logger (can be the same logger or separate)
session_logger = logging.getLogger("session")
session_logger.setLevel(logging.DEBUG)
session_handler = logging.StreamHandler()
session_handler.setFormatter(SessionFormatter())
session_logger.addHandler(session_handler)


# Custom formatter for main server
class ServerFormatter(logging.Formatter):
    def format(self, record):
        time_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"{time_str}: {record.levelname}: {record.getMessage()}"


# Root logger for server
server_logger = logging.getLogger("server")
server_logger.setLevel(logging.DEBUG)
server_handler = logging.StreamHandler()
server_handler.setFormatter(ServerFormatter())
server_logger.addHandler(server_handler)
