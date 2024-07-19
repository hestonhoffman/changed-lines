# make
SHELL = /bin/bash

.PHONY: tests
.DEFAULT_GOAL := tests

tests:
	python3 -m unittest discover -s ./tests/ -p 'test*.py' -v