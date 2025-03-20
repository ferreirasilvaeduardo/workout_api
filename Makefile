# Autor: Eduardo Cáceres de la Calle
# Fecha: 2021-09-29
# Descripción: Makefile para automatizar tareas de desarrollo
# Example: make run
# Regras 
run:
	@echo "Starting FastAPI server..."
	@PYTHONPATH=$(shell pwd) uvicorn workout_api.main:app --reload
create-migrations:
	@PYTHONPATH=$PYTHONPATH$(shell pwd) alembic revision --autogenerate -m $(d)
run-migrations:
	@PYTHONPATH=$PYTHONPATH:$(shell pwd) alembic upgrade head
format:
	isort .
	black .
	autopep8 --in-place --recursive .
lint:
	flake8 .
	pylint $(find . -name "*.py")
type-check:
	mypy .
	bandit -r .
test:
	pytest