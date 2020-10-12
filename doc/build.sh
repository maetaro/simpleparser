source venv/bin/activate
sphinx-apidoc -f -o source/. ../src/.
make html
