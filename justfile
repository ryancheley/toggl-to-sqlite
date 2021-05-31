# run tests via pytest, creates coverage report, and then opens it up
test:
    coverage run -m pytest
    coverage html
    open htmlcov/index.html