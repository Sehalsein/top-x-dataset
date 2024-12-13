SHELL := /bin/bash

dev:
	source .venv/bin/activate && fastapi dev app/main.py

consumer:
	source .venv/bin/activate && PYTHONPATH=./ python consumers/dataset_consumer.py
