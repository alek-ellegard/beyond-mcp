# Prime File System Scripts

Understand how to use the file system scripts for Kalshi market data.

## Variables

KALSHI_SCRIPTS_PATH_ROOT_DIR: `apps/3_file_system_scripts`
KALSHI_SCRIPTS_PATH_SCRIPTS_DIR: `apps/3_file_system_scripts/scripts/`

## Instructions

- Default to using `--json` flag for all commands.
- Prioritize high volume markets, series, and events.
- You can use `jq` to parse the JSON output.
- **IMPORTANT**: DO NOT read the scripts themselves.
  - ONLY read the scripts when running `<script.py> --help` doesn't give you the information you need.

## Workflow

1. READ @apps/3_file_system_scripts/README.md and @apps/3_file_system_scripts/scripts/
   - **IMPORTANT**: DO NOT read the scripts themselves. Only the directory structure.
2. Run the `Report` section.
2. As you work with the user, based on their request, run `<script.py> --help` to see the available options and then call the script with `uv run <script.py> <options>` to get the data you need.

## Report

Report your understanding of the file system scripts for Kalshi market data and when you'll use each script.
Clearly state that you understand you will not read the scripts themselves.