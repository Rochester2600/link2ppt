init:
    pip install pipenv
    pipenv install --dev

ci:
    pipenv run l2ppt.py
