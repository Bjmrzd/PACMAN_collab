SHELL := /bin/bash
PYTHON = python3
VENV = Pac_venv

run:
	@printf "Launching PacMan game ! \n\n"
	@$(PYTHON) pac-man.py
	@ rm -rf src/__pycache__

clean:
	@printf "Cleaning everything ! \n"
	@rm -rf src/__pycache__
	@rm -rf __pycache__
	@rm -rf .mypy_cache

install:
	@printf "Installing required packages ! \n\n"
	@pip install --upgrade pip
	@pip install -r requirements.txt

install_venv:
	@pip install --upgrade --require-virtualenv pip
	@pip install --require-virtualenv -r requirements.txt

venv:
	@printf "Creating the venv !\n"
	@python3.13 -m venv $(VENV)

erase:
	@rm -rf $(VENV)
	@printf "Virtual env is gone.\n"