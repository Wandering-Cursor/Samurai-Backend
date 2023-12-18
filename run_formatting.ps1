python -m pip install -r lint-requirements.txt --upgrade pip

isort .
ruff format .