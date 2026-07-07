#!/usr/bin/python3

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated

import typer
from termcolor import cprint

import optypes.types as types
from settings import settings
from utils.metric import get_metric
from utils.ping import ping_agent
from utils.uninstall import uninstall_function
from utils.update import update_function

app = typer.Typer(
    help="OpenHubble CLI",
    no_args_is_help=True,
    add_completion=False,
)


@dataclass
class AgentConfig:
    host: str = "127.0.0.1"
    port: int = 9703
    key: str = "apikey"
    use_https: bool = False


def load_config(path: Path | None) -> AgentConfig:
    config = AgentConfig()

    if path is None:
        return config

    with path.open("rb") as f:
        data = tomllib.load(f)

    return AgentConfig(
        host=data.get("host", config.host),
        port=data.get("port", config.port),
        key=data.get("key", config.key),
        use_https=data.get("use_https", config.use_https),
    )


def show_version(value: bool = True):
    if value:
        cprint(
            f"OpenHubble CLI {settings.project_version}",
            "cyan",
            attrs=["bold"],
        )

        raise typer.Exit()


@app.callback()
def main(
        version: Annotated[
            bool | None,
            typer.Option(
                "--version", "-v",
                callback=show_version,
                is_eager=True,
                help="Show application version"
            )
        ] = None
):
    pass


@app.command("version", rich_help_panel="CLI", help="Show application version")
def version():
    show_version()


@app.command("update", rich_help_panel="CLI", help="Update application")
def update(force: types.force = False):
    update_function(force)


@app.command("uninstall", rich_help_panel="CLI", help="Uninstall application")
def uninstall(force: types.force = False):
    uninstall_function(force)


@app.command("ping", rich_help_panel="Ping Agent", help="Ping Agent server")
def ping(
        host: types.host_type = "127.0.0.1",
        port: types.port_type = 9703,
        key: types.key_type = "apikey",
        use_https: types.use_https_type = False
):
    ping_agent(host, port, key, use_https)


@app.command("pingf", rich_help_panel="Ping Agent", help="Ping Agent server with a toml file")
def ping_file(config_file: types.config_file_type):
    conf = load_config(config_file)

    host = conf.host
    port = conf.port
    key = conf.key
    use_https = conf.use_https

    ping_agent(host, port, key, use_https)


@app.command("metric", rich_help_panel="Get Metrics", help="Get metric from agent")
def get_metrics(
        host: types.host_type = "127.0.0.1",
        port: types.port_type = 9703,
        key: types.key_type = "apikey",
        use_https: types.use_https_type = False,
        metric: types.metric_type = "agent.hostname"
):
    get_metric(host, port, key, use_https, metric)


@app.command("metricf", rich_help_panel="Get Metrics", help="Get metric from agent with a toml file")
def get_metrics_file(config_file: types.config_file_type, metric: types.metric_type = "agent.hostname"):
    conf = load_config(config_file)

    host = conf.host
    port = conf.port
    key = conf.key
    use_https = conf.use_https

    get_metric(host, port, key, use_https, metric)


if __name__ == "__main__":
    app()
