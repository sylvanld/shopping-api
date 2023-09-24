VENV:=.venv
HOST:=0.0.0.0
PORT:=8087

$(VENV):
	virtualenv -p python3 $(VENV)

requires-venv:
	@[ -d $(VENV) ] || make install

install: $(VENV)
	$(VENV)/bin/pip install -r requirements/lock.txt -r requirements/dev.txt

lock:
	virtualenv -p python3 .tmp-venv
	.tmp-venv/bin/pip install -r requirements/prod.txt
	.tmp-venv/bin/pip freeze > requirements/lock.txt
	rm -rf .tmp-venv

format: requires-venv
	$(VENV)/bin/isort shopping tests
	$(VENV)/bin/black --line-length 120 shopping tests

serve: requires-venv
	$(VENV)/bin/uvicorn --host $(HOST) --port $(PORT) --reload --factory shopping.api.factory:create_api

tests: requires-venv
	rm -rf tests/output && mkdir tests/output
	echo '<h1>Test results</h1><ul><li><a href="coverage">Coverage</a></li><li><a href="results">Results</a></li></ul>' > tests/output/index.html
	$(VENV)/bin/python -m pytest -vvv --cov=shopping/ --cov-report=html:tests/output/coverage --cov-fail-under=90 --html=tests/output/results/index.html tests/

lint: requires-venv
	$(VENV)/bin/isort --profile black --check shopping/ tests/
	$(VENV)/bin/black --line-length 120 --check shopping/ tests/
	$(VENV)/bin/flake8 --max-line-length 120 shopping/ tests/
