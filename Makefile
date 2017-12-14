init:
	pip install pipenv
	pipenv install --dev

test: 
	pipenv run python l2ppt.py -t

ci:
	pipenv run python l2ppt.py -t
