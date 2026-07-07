#!/usr/bin/python3

import subprocess
from pathlib import Path
from typing import Annotated

import requests
import typer
from art import text2art
from packaging.version import Version
from rich.console import Console
from rich.table import Table
from rich_gradient import Gradient
from termcolor import cprint

from settings import settings

app = typer.Typer(
    help="OpenHubble CLI",
    no_args_is_help=True,
    add_completion=True,
)

console = Console()


# -------------------------------------------------------------------
# Art
# -------------------------------------------------------------------


def print_art():
    openhubble_art = text2art("OpenHubble")
    cli_art = text2art("CommandLine")

    palette = [
        "#3674B5",
        "#578FCA",
        "#A1E3F9",
        "#D1F8EF",
    ]

    print()

    console.print(
        Gradient(openhubble_art, colors=palette, justify="center")
    )

    console.print(
        Gradient(cli_art, colors=palette[::-1], justify="center")
    )


# -------------------------------------------------------------------
# GitHub
# -------------------------------------------------------------------

def get_github_releases():
    response = requests.get(
        "https://api.github.com/repos/OpenHubble/cli/releases",
        timeout=10
    )
    response.raise_for_status()
    return response.json()


def check_for_updates():
    latest_release = get_github_releases()[0]

    current_version = settings.project_version
    latest_version = latest_release["tag_name"]
    latest_name = latest_release["name"]
    latest_url = latest_release["html_url"]

    if not Version(latest_version) > Version(current_version):
        return {
            'new': False
        }
    else:
        return {
            'new': True,
            'latest':
                {
                    'latest_version': latest_version,
                    'latest_name': latest_name,
                    'latest_url': latest_url
                }
        }


def show_version():
    cprint(
        f"OpenHubble CLI {settings.project_version}",
        "cyan",
        attrs=["bold"],
    )


def version_callback(value: bool):
    if value:
        show_version()
        raise typer.Exit()


# -------------------------------------------------------------------
# UI
# -------------------------------------------------------------------

@app.callback()
def main(
        version: Annotated[
            bool | None,
            typer.Option(
                "--version", "-v",
                callback=version_callback,
                is_eager=True,
                help="Show application version"
            )
        ] = None
):
    pass


# -------------------------------------------------------------------
# Commands
# -------------------------------------------------------------------

@app.command("version", rich_help_panel="CLI", help="Show application version")
def version():
    show_version()


@app.command("update", rich_help_panel="CLI", help="Update application")
def update():
    check_update = check_for_updates()

    if not check_update['new']:
        cprint(f"You are using latest version of OpenHubble CLI: {settings.project_version}")
        raise typer.Exit()

    latest = check_update['latest']

    table = Table("New version is available!")
    table.add_row(f"{latest["latest_name"]}")
    table.add_row(f"Version: {latest["latest_version"]}")
    table.add_row(f"Release note: {latest["latest_url"]}")

    console.print(table)

    cprint("")

    cprint(f"You are using version {settings.project_version}", "yellow")
    confirm = typer.confirm(f"Do you want to update {latest["latest_version"]}")

    cprint("")

    if not confirm:
        cprint("Run 'openhubble update' whenever you're ready.", "yellow")
        raise typer.Abort()

    cprint(f"Updating OpenHubble CLI to version {latest["latest_version"]}", "blue")

    subprocess.run(
        ["sudo", Path("/opt/openhubble-cli/scripts/update.sh")],
        check=True,
    )

    cprint("Updated successfully.", "green")


@app.command("uninstall", rich_help_panel="CLI", help="Uninstall application")
def uninstall():
    confirm = typer.confirm("Do you really want to uninstall OpenHubble CLI?")

    cprint("")

    if not confirm:
        cprint("Thanks for keeping OpenHuble CLI.", "green")
        raise typer.Abort()

    subprocess.run(
        ["sudo", Path("/opt/openhubble-cli/scripts/uninstall.sh")],
        check=True,
    )

    cprint("Uninstalled successfully.", "green")


@app.command("ping", rich_help_panel="Agent", help="Ping Agent server")
def ping(
        host: Annotated[
            str, typer.Option(
                "--host", "-H",
                help="Host running Agent",
                prompt="Enter Agent host"
            )
        ] = "127.0.0.1",
        port: Annotated[
            int, typer.Option(
                "--port", "-P",
                help="Port that Agent expose",
                prompt="Enter Agent port"
            )
        ]
        = 9703,
        key: Annotated[
            str | None, typer.Option(
                "--key", "-K",
                help="API Key you defined in Agent",
                prompt="Enter the Agent API Key"
            )
        ] = "apikey",
        use_https: Annotated[
            bool, typer.Option(
                "--use-https",
                help="Use connection over HTTPS with Agent",
                prompt="Do you want to use HTTPS",
                is_eager=True
            )
        ] = False
):
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


@app.command("get", rich_help_panel="Agent", help="Get metric from agent")
def get_metric_command(
        host: Annotated[
            str, typer.Option(
                "--host", "-H",
                help="Host running Agent",
                prompt="Enter Agent host"
            )
        ] = "127.0.0.1",
        port: Annotated[
            int, typer.Option(
                "--port", "-P",
                help="Port that Agent expose",
                prompt="Enter Agent port"
            )
        ]
        = 9703,
        key: Annotated[
            str | None, typer.Option(
                "--key", "-K",
                help="API Key you defined in Agent",
                prompt="Enter the Agent API Key"
            )
        ] = "apikey",
        use_https: Annotated[
            bool, typer.Option(
                "--use-https",
                help="Use connection over HTTPS with Agent",
                prompt="Do you want to use HTTPS",
                is_eager=True
            )
        ] = False,
        metric: Annotated[
            str, typer.Option(
                "--metric", "-M",
                help="Metric you want to get from Agent",
                prompt="Enter the metric"
            )
        ] = "agent.hostname"
):
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


if __name__ == "__main__":
    app()
