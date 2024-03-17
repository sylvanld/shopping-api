VENV:=.venv
HOST:=0.0.0.0
DEBUG?=true

SHOPPING_API_PORT ?= 8087

export

.DEFAULT_GOAL=help

$(VENV):
	virtualenv -p python3 $(VENV)

requires-venv:
	@[ -d $(VENV) ] || make install

help: ## Show this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

##@ Development targets

install: $(VENV) ## Install development dependencies in a virtualenv
	$(VENV)/bin/pip install -r requirements/dev.txt

lock: ## Pin latest versions of dependencies compatible with requirements/prod in requirements/lock file
	virtualenv -p python3 .tmp-venv
	.tmp-venv/bin/pip install -r requirements/prod.txt
	.tmp-venv/bin/pip freeze > requirements/lock.txt
	rm -rf .tmp-venv

format: requires-venv ## Format code according to project conventions
	$(VENV)/bin/isort shopping tests
	$(VENV)/bin/black --line-length 120 shopping tests

serve: requires-venv ## Start API server in debug mode
	$(VENV)/bin/uvicorn --host $(HOST) --port $(SHOPPING_API_PORT) shopping.__main__:api


##@ Validation targets

tests: requires-venv ## Run unit and functional tests
	rm -rf tests/output && mkdir tests/output
	echo '<h1>Test results</h1><ul><li><a href="coverage">Coverage</a></li><li><a href="results">Results</a></li></ul>' > tests/output/index.html
	$(VENV)/bin/python -m pytest -vvv --cov=shopping/ --cov-report=html:tests/output/coverage --cov-fail-under=30 --html=tests/output/results/index.html tests/

lint: requires-venv ## Check code formatting and quality
	$(VENV)/bin/isort --profile black --check shopping/ tests/
	$(VENV)/bin/black --line-length 120 --check shopping/ tests/
	$(VENV)/bin/flake8 --max-line-length 120 shopping/ tests/

##@ Docker targets

build:
	@docker build -t sylvanld/shopping-api:latest .

start:
	@docker run -d --name shopping-api -p 8000:8000 sylvanld/shopping-api:latest

stop:
	@docker stop shopping-api && docker rm shopping-api

shell:
	@docker exec -it shopping-api sh
