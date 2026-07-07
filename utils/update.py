import subprocess
from pathlib import Path

import requests
import typer
from packaging.version import Version
from rich.console import Console
from rich.table import Table
from termcolor import cprint

from settings import settings

console = Console()


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


def do_update():
    subprocess.run(
        ["sudo", Path("/opt/openhubble-cli/scripts/update.sh")],
        check=True,
    )

    cprint("Updated successfully.", "green")


def update_function(force: bool):
    if force:
        do_update()
        raise typer.Exit()

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

    do_update()
