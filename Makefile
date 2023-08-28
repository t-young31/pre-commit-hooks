.PHONY: *
SHELL:=/bin/bash

dev: python_version_is_39
	if [ ! -d .venv ]; then python3 -m venv .venv; fi
	source ".venv/bin/activate"
	pip install -e .[dev]
	pre-commit install
	echo ""
	echo 'Activate with: source ".venv/bin/activate"'

python_version_is_39:
	if ! python3 --version | grep -q "3.9"; then \
  		echo "Must be using Python 3.9" && exit 1; \
  	fi

.SILENT: # silence all targets
