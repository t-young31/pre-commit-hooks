# pre-commit-hooks
[pre-commit](https://pre-commit.com/) hooks to run shared utilities

```yaml
repos:
  - repo: https://github.com/t-young31/pre-commit-hooks
    rev: 0.1.1  # Use the ref you want to point at
    hooks:
    - id: stale-version
```

## Hooks

### [stale-version](https://github.com/t-young31/pre-commit-hooks/blob/main/src/tyhooks/stale_version.py)
Ensures that any changes in a source directory are associated with a version
increment. Works with Python projects

```yaml
- id: stale-version
  args: ["--upstream", "origin/master", "--dirs", "src|lib"]
```
- `--upstream`: Upstream git branch to check the diff against. Default: `origin/main`
- `--dirs`: Pipe seperated list of directories to consider source directories. Default: `src`. Example: `src|lib`

## Contributing

- Fork this repository
- Clone and run `make dev` to create a [venv](https://docs.python.org/3/library/venv.html)
- Activate the environment with `source .venv/bin/activate`
- Commit your changes, push and open pull request against `t-young31/main`
