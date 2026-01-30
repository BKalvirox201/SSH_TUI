import asyncio
import asyncssh

from src.ssh_session import MySSHServerSession


class MySSHServer(asyncssh.SSHServer):
    def session_requested(self) -> asyncssh.SSHServerSession:
        return MySSHServerSession()

    def begin_auth(self, username: str) -> bool:
        return False


async def start_server() -> None:
    await asyncssh.create_server(
        MySSHServer,
        "",
        8022,
        server_host_keys=["ssh_key"],
    )


async def main():
    await start_server()
    await asyncio.Event().wait()  # keep running forever


if __name__ == "__main__":
    asyncio.run(main())
