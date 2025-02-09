# GitHub-Todoist Syncer

A lightweight utility to sync GitHub issues and Todoist tasks. 

Syncing logic:
- For each **open** GitHub issue assigned to the user, if a Todoist task with the issue URL in the description **does not** exist, create one.
- For each **closed** GitHub issue assigned to the user, if a Todoist task with the issue URL in the description **exists**, close it.

## Getting Started

1. Clone or fork this repo
1. Add tokens to `.env.template` and rename to `.env`
1. Install [uv](https://docs.astral.sh/uv/getting-started/) if not already installed
1. Run `scripts/sync.sh`
1. If you want to schedule routine syncs, create a timed job using `launchd`, `crontab`, etc. For example, to sync at 10am every day using `launchd` (on a Mac), create a plist file (eg, `com.user.github-todoist-sync.plist`) in `~/Library/LaunchAgents/`. (Depending on the repo's location on your machine, you may need to change the path to `sync.sh`.)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.user.github-todoist-sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>~/github-todoist-sync/scripts/sync.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>10</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
</dict>
</plist>
```

## Development

### Dependencies

#### Setting up the environment

This project uses [uv](https://docs.astral.sh/uv/getting-started/) for package and environment management. After following the installation instructions on the `uv` website, run the following commands from the project root directory:

1. `uv sync`
2. `. .venv/bin/activate`

#### Adding new dependencies

Run `uv add <package name>` from within the project folder to add a project dependency, or `uv add --dev <package name>` for a dev dependency.

### Formatting

If using Visual Studio Code, install [the Ruff extension](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff), and make sure your `.vscode/settings.json` looks like this:

```JSON
{
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "explicit",
            "source.organizeImports": "explicit"
        },
        "editor.defaultFormatter": "charliermarsh.ruff"
    }
}
```

If you don't want to have `ruff` auto-format on save, you can also set `"source.fixAll"` to `"never"`.

To run the same three linters that the CI runs:

* `uv run ruff check .`
* `uv run ruff format --check .`
* `uv run ruff check --select I .`

## CI/CD

The project is configured to run `ruff` (`.github/workflows/lint.yml`), `bandit` and `trivy` (`.github/workflows/security.yml`), and unit tests (`.github/workflows/test.yml`) when creating a PR.
