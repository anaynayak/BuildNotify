Local setup:

* virtualenv -p python3 venv
* source venv/bin/activate.fish
* `tox` for running tests 
* `pip install -e .` for installing locally. Use `python buildnotifyapplet.py` to launch
* `paver mk_resources` is used to regenerate source files corresponding to icons/dialogs.

Paver commands can be viewed by running `paver -h`. Run `pip install paver` if not installed.

### Packaging

Dependencies for creating a pip/deb package (use virtualenv)

```
pip install paver
pip install stdeb
pip install twine
pip install keyrings.alt
apt-get install debhelper dput
```