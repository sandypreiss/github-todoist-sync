# Python Project Basic Template - `uv` edition

<img align="right" width="64" height="64" src="https://astral.sh/static/SVG/UV.svg">

A python project template ready to go with the `uv` python package and project manager.

### 📒 Includes

- [`uv` project](https://docs.astral.sh/uv/concepts/projects/) setup
- Basic testing setup with `pytest`
- python based `.gitignore`
- `ruff` as a linter, with many additional linters added.
- `ruff` as a formatter
- CI/CD through GitHub Actions
  - Runs `ruff` to lint and format your code
  - Runs security scans with `bandit` (python) and `trivy` (dependencies, secrets)
  - Runs test suite with `pytest`
- [README template](README-template.md)

While this template does give you an out-of-the-box package, you can also pick and choose relevant elements like GitHub Actions or project settings to include in your own project.

## 🏗️ Getting Started with `uv`

1. [Install `uv`](https://docs.astral.sh/uv/getting-started/installation/) if you don't yet have it. This template was created with version `0.3.3`.
2. Run `uv sync`
    * To initialize with a specific version of python, you can run `uv sync --python 3.12`
    * If you don't specify, `uv` will initialize based on the `requires-python` definition in `pyproject.toml`. For this template, it will be `3.13` since it's set to `">=3.10"`
3. Remove the existing `cowsay` dependency `uv remove cowsay` (it's there for demonstration purposes).
4. Add your own dependencies with `uv add <package>`

🔗 [`uv` Docs](https://docs.astral.sh/uv/)

### Getting Started with `devcontainers`

With the [dev containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) installed in VSCode, open the command palette (`CMD-SHIFT-P`) then select `Dev Containers: Rebuild and Reopen in Container`.

You may need to modify the version of python used to match your requirements in `pyproject.toml` within the assocaited `.devcontainer/Dockerfile`.

> [!NOTE]  
> If you are intending on using python with multiple languages or multiple python services with `docker compose`, [pypath](https://github.com/rti-international/pypath) is a more suitable solution.

🔗 [devcontainers Docs](https://code.visualstudio.com/docs/devcontainers/containers)

### Transitioning to your own project name

All files and folders will still have the `my_project` name in them. You'll likely want to replace these with a relevant project name. You can use the two commands below to replace all instances of `my_project` with `new_project_name` within all files, as well as rename the directory for the package.

```bash
# tested on macOS
# replace within files
find . -type f \( -name "*.py" -o -name "*.toml" \) -exec sed -i '' -e 's/my_project/new_project_name/g' {} +
# replace folder names
find . -depth -name '*my_project*' -exec bash -c 'mv "$1" "$(dirname "$1")/$(basename "$1" | sed "s/my_project/new_project_name/g")"' _ {} \;
```

Now that you've renamed the project, you should reinstall your package locally under the new name.

### ⚙️ Recommend VSCode Settings

Requires the `python` and `ruff` extensions.

```json
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.fixAll": "never",
            "source.organizeImports": "explicit"
        },
        "editor.defaultFormatter": "charliermarsh.ruff"
    },
```