import requests
from termcolor import cprint


def get_metric(host: str, port: int, key: str, use_https: bool, metric: str):
    protocol = "https" if use_https else "http"

    url = (
        f"{protocol}://{host}:{port}"
        f"/api/get?metric={metric}"
    )

    try:
        r = requests.get(
            url,
            headers={"X-API-KEY": key},
            timeout=10
        )

        r.raise_for_status()

        data = r.json()

        if "metric" in data:
            cprint(f"Metric: {data['metric']}", "green")
        else:
            cprint("Unexpected response.", "yellow")

    except requests.RequestException as e:
        cprint(f"Error: {e}", "red")
