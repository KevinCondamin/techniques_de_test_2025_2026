test :
	pytest

unit_test :
	pytest ./tests/unit

perf_test :
	pytest ./tests/perf

coverage :
	coverage run -m pytest
	coverage html

lint :
	ruff check main.py

doc :
	pdoc3 . --html --force