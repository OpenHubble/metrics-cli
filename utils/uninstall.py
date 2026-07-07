import subprocess
from pathlib import Path

import typer
from termcolor import cprint


def do_uninstall():
    subprocess.run(
        ["sudo", Path("/opt/openhubble-cli/scripts/uninstall.sh")],
        check=True,
    )

    cprint("Uninstalled successfully.", "green")


def uninstall_function(force: bool):
    if force:
        do_uninstall()
        raise typer.Exit()

    confirm = typer.confirm("Do you really want to uninstall OpenHubble CLI?")

    cprint("")

    if not confirm:
        cprint("Thanks for keeping OpenHuble CLI.", "green")
        raise typer.Abort()

    do_uninstall()
