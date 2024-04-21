# pre-commit-hooks
[pre-commit](https://pre-commit.com/) hooks

```yaml
repos:
  - repo: https://github.com/t-young31/pre-commit-hooks
    rev: 0.1.2  # Use the ref you want to point at
    hooks:
    - id: stale-version
    - id: no-todos
    - id: tf-deps
```

## 🪝 Hooks

### [stale-version](./src/tyhooks/stale_version.py)
Ensures that any changes in a source directory trigger a version
increment. Works with {Python, Rust, Helm} projects. For example,
to check changes against `origin/master` in `src` and `lib` directories use:

```yaml
- id: stale-version
  args: ["--upstream", "origin/master", "--dirs", "src|lib"]
```
- `--upstream`: Upstream git branch to check the diff against. Default: `origin/main`
- `--dirs`: Pipe seperated list of directories to consider source directories. Default: `src`. Example: `src|lib`

### [no-todos](./src/tyhooks/no_todos.py)
Ensures that there are no "TODO" comments anywhere in any file


### [tf-deps](./src/tyhooks/tf_deps.py)
Prompts to check updates on a schedule for pinned versions of
dependencies in `.tf` files.

```yaml
- id: tf-deps
  args: ["--frequency", "weekly"]  # default
```

## 🤝 Contributing

- Fork this repository
- Clone and run `make dev` to create a [venv](https://docs.python.org/3/library/venv.html)
- Activate the environment with `source .venv/bin/activate`
- Commit your changes, push and open pull request against `t-young31/main`
