SHELL := /bin/bash

dev:
	source .venv/bin/activate && fastapi dev app/main.py

start:
	source .venv/bin/activate && fastapi run app/main.py

consumer:
	source .venv/bin/activate && PYTHONPATH=./ python consumers/dataset_consumer.py

ingest:
	source .venv/bin/activate && python scripts/ingest_data.py $(ARGS)

install:
	python3 -m venv .venv
	source .venv/bin/activate && pip install -r requirements.txt