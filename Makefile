.PHONY: quality style clean

check_dirs := storyteller

quality:
	black --check $(check_dirs)
	isort --check-only $(check_dirs)
	flake8 $(check_dirs) --max-line-length 119

style:
	black $(check_dirs)
	isort $(check_dirs)

clean:
	rm -rf out

run:
	python -m storyteller
