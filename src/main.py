"""API Main."""

from src.server import APIServerConfig, Server

if __name__ == "__main__":
    Server().run(api_server_config=APIServerConfig())
