import asyncio
import signal

import asyncssh

from src.core.logging import server_logger
from src.core.session import SSHServerSession


class MySSHServer(asyncssh.SSHServer):
    def session_requested(self) -> asyncssh.SSHServerSession:
        return SSHServerSession()

    def begin_auth(self, username: str) -> bool:
        return False


async def start_server():
    """
    Start the asyncssh server using the documented pattern.
    Note: create_server returns an `SSHListener` / server object.
    """
    server_logger.info("SSH server starting on port 8022")
    return await asyncssh.create_server(
        MySSHServer,
        "",
        8022,
        server_host_keys=["ssh/ssh_host_key"],
    )


async def main():
    # Event to wait for shutdown signal
    stop_event = asyncio.Event()
    loop = asyncio.get_running_loop()

    # Register signals
    loop.add_signal_handler(signal.SIGINT, stop_event.set)
    loop.add_signal_handler(signal.SIGTERM, stop_event.set)

    server = await start_server()
    server_logger.info("Server running. Press Ctrl-C to stop.")

    await stop_event.wait()
    server_logger.info("Shutting down server...")
    server.close()

    await server.wait_closed()
    server_logger.info("Server stopped by user")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as exc:
        server_logger.fatal(f"Server crashed: {exc}")
