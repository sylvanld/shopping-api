VENV:=.venv
HOST:=0.0.0.0
PORT:=8087

$(VENV):
	virtualenv -p python3 $(VENV)

requires-venv:
	@[ -d $(VENV) ] || { echo "No virtualenv found, create it with:"; echo "\n   make install\n"; exit 1; }

install: $(VENV)
	$(VENV)/bin/pip install -r requirements/lock.txt -r requirements/dev.txt

lock:
	virtualenv -p python3 .tmp-venv
	.tmp-venv/bin/pip install -r requirements/prod.txt
	.tmp-venv/bin/pip freeze > requirements/lock.txt
	rm -rf .tmp-venv

serve: requires-venv
	$(VENV)/bin/uvicorn --host $(HOST) --port $(PORT) --reload --factory shopping.api.factory:create_api
