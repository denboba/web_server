IS_VENV_ACTIVE=false
ifdef VIRTUAL_ENV
	IS_VENV_ACTIVE=true
endif

enforce_venv:
ifeq ($(IS_VENV_ACTIVE), false)
	$(error "You must activate your virtual environment. Exiting...")
endif

create_venv:
	python -m venv venv

install: enforce_venv requirements.txt
	python -m pip install -r requirements.txt

run_server: enforce_venv
	flask run

run_tests: enforce_venv
	python checker/checker.py

