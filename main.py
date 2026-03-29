import asyncio
import signal

import asyncssh

from src.core.logging import server_logger
from src.core.session.session import SSHServerSession
from src.core.session.session_manager import SSHSessionManager


class SSHServer(asyncssh.SSHServer):
    def __init__(self):
        self.session_manager = SSHSessionManager()

    def session_requested(self):
        return SSHServerSession(self.session_manager)

    def begin_auth(self, username):
        return False


async def start_server():
    """
    Start the asyncssh server using the documented pattern.
    Note: create_server returns an `SSHListener` / server object.
    """
    server_logger.info("SSH server starting on port 8022")
    return await asyncssh.create_server(
        SSHServer,
        "",
        8022,
        server_host_keys=["ssh/ssh_host_key"],
    )


async def main():

    stop_event = asyncio.Event()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, stop_event.set)
    loop.add_signal_handler(signal.SIGTERM, stop_event.set)

    # Explicitly create a server factory and keep a reference
    server_factory = SSHServer()
    listener = await asyncssh.create_server(
        lambda: server_factory,
        host="0.0.0.0",
        port=8022,
        server_host_keys=["./ssh/ssh_host_key"],
    )

    server_logger.info("Server running... Press Ctrl-C to stop")
    await stop_event.wait()

    server_logger.info("Shutting down sessions...")
    await server_factory.session_manager.close_all_sessions()

    server_logger.info("Closing listener...")
    listener.close()
    await listener.wait_closed()
    server_logger.info("Server stopped.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        server_logger.fatal(f"Server crashed: {exc}")
