import socket
import subprocess
import time


def wait_for_port(host: str, port: int, timeout: float = 30.0) -> None:
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        try:
            with socket.create_connection((host, port), timeout=1):
                return
        except OSError:
            time.sleep(0.2)
    raise TimeoutError(f"Showdown ne répond pas sur {host}:{port} après {timeout}s")


def run_showdown_server() -> subprocess.Popen[bytes]:
    log_file = open("pokemon_showdown.log", "w")

    process = subprocess.Popen(
        ["node", "pokemon-showdown", "start", "--no-security"],
        cwd="vendor/pokemon-showdown/",
        stdout=log_file,
        stderr=log_file,
    )

    try:
        wait_for_port("localhost", 8000)
    except TimeoutError:
        process.terminate()
        raise

    return process


def close_showdown_server(process: subprocess.Popen[bytes]):
    print("Stopping the server...")
    process.terminate()
    process.wait()
    print("Server stopped.")