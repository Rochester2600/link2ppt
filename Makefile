init:
	pip install pipenv
	pipenv install --dev

ci:
	pipenv run python l2ppt.py
