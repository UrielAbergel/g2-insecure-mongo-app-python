# tests/conftest.py

import threading
import time

import pytest_asyncio
from httpx import AsyncClient
from werkzeug.serving import make_server

from app import create_app


class ServerThread(threading.Thread):
    def __init__(self, app, host="127.0.0.1", port=5001):
        super().__init__()
        self.srv = make_server(host, port, app)
        self.ctx = app.app_context()
        self.daemon = True

    def run(self):
        self.ctx.push()
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()


@pytest_asyncio.fixture(scope="module")
async def client():
    app = create_app()
    server = ServerThread(app)
    server.start()
    time.sleep(0.5)

    async with AsyncClient(base_url="http://127.0.0.1:5001") as ac:
        yield ac

    server.shutdown()
