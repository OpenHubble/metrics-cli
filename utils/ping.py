import requests
from termcolor import cprint


def ping_agent(host: str, port: int, key: str, use_https: bool):
    protocol = "https" if use_https else "http"

    url = f"{protocol}://{host}:{port}/api/ping"

    try:
        r = requests.get(
            url,
            headers={"X-API-KEY": key},
            timeout=10
        )

        r.raise_for_status()

        if r.json().get("message") == "pong":
            cprint("Agent is running.", "green")
        else:
            cprint("Unexpected response.", "yellow")

    except requests.RequestException as e:
        cprint(f"Error: {e}", "red")
