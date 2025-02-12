import json
from scripts.common import write_file
import argparse
from pathlib import Path

my_parser = argparse.ArgumentParser(prog="generate-config", description="Generate GH Actions configs")

my_parser.add_argument(
    "--target",
    metavar="STRING",
    type=str,
    help="Target marketplace",
    default="vscode-marketplace",
)

my_parser.add_argument(
    "--marketplace",
    metavar="STRING",
    type=str,
    help="Pretty name of target marketplace",
    default="VSCode Marketplace",
)

my_parser.add_argument(
    "--approx-extensions",
    metavar="INT",
    type=int,
    help="Approximate number of extensions on the target",
    required=True
)

my_parser.add_argument(
    "--block-size",
    metavar="INT",
    type=int,
    help="Block size",
    default = 100,
)

my_parser.add_argument(
    "--block-limit",
    metavar="INT",
    type=int,
    help="Approximate number of extensions on the target",
    default=25
)

my_parser.add_argument(
    "--max-attempts",
    metavar="INT",
    type=int,
    help="Number of attempts to run a step",
    default=3
)

my_parser.add_argument(
    "--retry-wait-minutes",
    metavar="INT",
    type=int,
    help="Timeout before step retry",
    default=60
)

my_parser.add_argument(
    "--timeout-minutes",
    metavar="INT",
    type=int,
    help="Timeout before cancelling a command",
    default=300
)

args = my_parser.parse_args()

APPROX_EXTENSIONS = args.approx_extensions
TARGET = args.target
MARKETPLACE = args.marketplace
BLOCK_SIZE = args.block_size
BLOCK_LIMIT = args.block_limit
APPROX_BLOCKS = int((APPROX_EXTENSIONS + (BLOCK_SIZE * BLOCK_LIMIT)) / (BLOCK_SIZE * BLOCK_LIMIT))
MAX_ATTEMPTS = args.max_attempts
TIMEOUT_MINUTES = args.timeout_minutes
RETRY_WAIT_SECONDS = args.retry_wait_minutes * 60

include = [
    {
        "ACTION_ID": i + 1,
        "FIRST_BLOCK": i * BLOCK_LIMIT + 1,
        "MARKETPLACE": MARKETPLACE,
        "TARGET": TARGET,
        "BLOCK_SIZE": BLOCK_SIZE,
        "BLOCK_LIMIT": BLOCK_LIMIT,
        "MAX_ATTEMPTS": MAX_ATTEMPTS,
        "TIMEOUT_MINUTES": TIMEOUT_MINUTES,
        "RETRY_WAIT_SECONDS": RETRY_WAIT_SECONDS,
    }
    for i in range(APPROX_BLOCKS)
]
NUMBER_JOBS = len(include)

nvfetch = {
    "include": include,
}

configs_dir = Path(".github") / "workflows" / "configs" / TARGET
write_file(
    configs_dir / "nvfetch.json",
    str(json.dumps(nvfetch, indent=2)),
)

combine = {
    "include": [
        {
            "TARGET": TARGET,
            "MARKETPLACE": MARKETPLACE,
            "NUMBER_JOBS": NUMBER_JOBS,
        }
    ]
}

write_file(
    configs_dir / "combine.json",
    str(json.dumps(combine, indent=2)),
)
