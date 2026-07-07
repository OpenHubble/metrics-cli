from pathlib import Path
from typing import Annotated

import typer

host_type = Annotated[
    str, typer.Option(
        "--host", "-H",
        help="Host running Agent",
        prompt="Enter Agent host"
    )
]
port_type = Annotated[
    int, typer.Option(
        "--port", "-P",
        help="Port that Agent expose",
        prompt="Enter Agent port"
    )
]
key_type = Annotated[
    str, typer.Option(
        "--key", "-K",
        help="API Key you defined in Agent",
        prompt="Enter the Agent API Key"
    )
]
use_https_type = Annotated[
    bool, typer.Option(
        "--use-https",
        help="Use connection over HTTPS with Agent",
        prompt="Do you want to use HTTPS",
    )
]
metric_type = Annotated[
    str, typer.Option(
        "--metric", "-M",
        help="Metric you want to get from Agent",
        prompt="Enter the metric"
    )
]
config_file_type = Annotated[
    Path,
    typer.Option(
        "--file", "-F",
        help="Load Agent configuration from a TOML file",
        exists=True,
        readable=True,
    ),
]
force = Annotated[
    bool,
    typer.Option(
        "--force", "-F",
        help="Force doing with out confirmation"
    )
]
