import subprocess
from pathlib import Path

import typer
from termcolor import cprint


def uninstall_function():
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
