#!/usr/bin/env python3
"""Install this repository's subagents into a single directory."""

import argparse
from pathlib import Path
import shutil
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "target",
        nargs="?",
        default="~/.codex/agents",
        help="destination directory (default: ~/.codex/agents); matching files are overwritten",
    )
    args = parser.parse_args()
    source = Path(__file__).resolve().parent / "categories"
    agents = sorted(source.rglob("*.toml"))
    if not agents:
        parser.error(f"no subagent definitions found in {source}")

    names = set()
    for agent in agents:
        if agent.name in names:
            parser.error(f"duplicate agent filename: {agent.name}")
        names.add(agent.name)

    try:
        target = Path(args.target).expanduser().resolve()
        target.mkdir(parents=True, exist_ok=True)
        for agent in agents:
            shutil.copy2(agent, target / agent.name)
    except (OSError, RuntimeError) as error:
        print(f"Installation failed: {error}", file=sys.stderr)
        return 1

    print(f"Installed {len(agents)} subagents into {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
