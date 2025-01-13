# project-name

## Development

### Dependencies

#### Setting up the environment

This project uses [uv](https://docs.astral.sh/uv/getting-started/) for package and environment management. After following the instructions on the `uv` website to get it setup, simply run the following commands from the project root directory:

1. `. .venv/bin/activate` (I've found it helpful to alias the first command to something easier to remember like `activate`)
2. `uv sync`

Once you've activated your virtual environment, you can run Python commands like normal. The only caveat is adding dependencies since you can't run `pip install x`. Instead refer to the section below for adding new dependencies.

#### Adding new dependencies

Run `uv add <package name>` from within the project folder to add a project dependency, or `uv add --dev <package name>` for a dev dependency. Dev dependencies are dependencies that you'd only need to develop or run a project locally. This would be packages for exploration or formatting like jupyter notebooks, ruff, etc. Basically, if you wouldn't need to install it in a deployed docker container, it's probably a dev dependency.

#### Working with contributors not using `uv`

If working with contributors who do not have `uv` installed and instead need to install dependencies with a `requirements.txt` file, you can run the below command to generate that file:

```shell
uv export --format requirements-txt -o requirements.txt --no-hashes
```

## Formatting

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

The project is automatically configured to run `ruff` (`.github/workflows/lint.yml`) when creating a PR.
