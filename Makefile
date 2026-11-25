SHELL := /bin/bash
PYTHON = python3
VENV = Pac_venv

run:
	@clear
	@printf "Launching PacMan game ! \n\n"
	@$(PYTHON) pac-man.py config.json
	@rm -rf src/__pycache__
	@make clean

clean:
	@printf "Cleaning everything ! \n"
	@rm -rf src/__pycache__
	@rm -rf __pycache__
	@rm -rf .mypy_cache
	@rm -rf mazegenerator/__pycache__
	@rm -rf game_files/__pycache__

install:
	@printf "\nInstalling required packages ! \n\n"
	@python -m pip install --upgrade pip
	@pip install --upgrade pip --quiet
	@pip install -r requirements.txt --quiet

venv:
	@printf "Creating the venv !\n"
	@python -m venv $(VENV)

erase:
	@rm -rf $(VENV)
	@printf "Virtual env is gone.\n"

lint: 
	@flake8 . &&  mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

package:
	pyinstaller --onefile --name Pacman pac-man.py --add-data "game_files:game_files" --add-data "config.json:config.json"
	cp config.json ./dist/config.json