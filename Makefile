test:
	python -m pytest ./src/tests

run:
	python ./proxy.py

.PHONY: test run
