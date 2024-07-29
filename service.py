from __future__ import annotations

from asgi_proxy import asgi_proxy

import os
import time
import bentoml
import socket
import subprocess


class TabbyServer:
    def __init__(self) -> None:
        self.launcher = subprocess.Popen(
            [
                "tabby",
                "serve",
                "--port",
                "8000",
            ]
        )

    def ready(self) -> bool:
        try:
            socket.create_connection(("127.0.0.1", 8000), timeout=1).close()
            return True
        except (socket.timeout, ConnectionRefusedError):
            # Check if launcher webserving process has exited.
            # If so, a connection can never be made.
            retcode = self.launcher.poll()
            if retcode is not None:
                raise RuntimeError(f"launcher exited unexpectedly with code {retcode}")
            return False

    def wait_until_ready(self) -> None:
        while not self.ready():
            time.sleep(1.0)


app = asgi_proxy("http://127.0.0.1:8000")


@bentoml.service(
    resources={"cpu": "1"},
    traffic={"timeout": 10},
)
@bentoml.mount_asgi_app(app, path="/")
class Tabby:
    @bentoml.on_deployment
    def download_tabby_dir():
        if os.system("rclone sync r2:/tabby-cloud-managed/internal/tabby-demo ~/.tabby") == 0:
            print("Downloaded tabby directory from remote")
        else:
            raise RuntimeError("Failed to download tabby directory")

    @bentoml.on_shutdown
    def upload_tabby_dir(self):
        if os.system("rclone sync ~/.tabby r2:/tabby-cloud-managed/internal/tabby-demo") == 0:
            print("Uploaded tabby directory to remote")
        else:
            raise RuntimeError("Failed to upload tabby directory")

    def __init__(self) -> None:
        # Start the server subprocess.
        self.server = TabbyServer()

        # Wait for the server to be ready.
        self.server.wait_until_ready()