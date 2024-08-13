# Contributing

## quickstart

### one-time setup

__system-wide__

- __install pipx__
- __install build dependencies__ for pyenv
  https://github.com/pyenv/pyenv/wiki#suggested-build-environment

__user-specific__

```SHELL
# install dev tools
pipx install pdm pre-commit tox
pipx inject pdm pdm-autoexport
pipx inject tox virtualenv-pyenv

# OS-independent Python versions
curl https://pyenv.run | bash
pyenv install 3.10
pyenv install 3.11
pyenv install 3.12
```

### repository setup

```SHELL
# install pre-commit hooks
for hook_type in pre-commit commit-msg post-commit pre-push ; do
    pre-commit install --allow-missing-config --hook-type $hook_type
done

# install package dependencies
pdm install
```

### testing

The entire test suite (unit tests & compatibility tests) can be triggered
by running

```SHELL
scripts/run_tests
```

You have successfully run all tests when the output ends with:

```
----------------------------------------------------------------------
If you reached this far you passed. Congratulations!
----------------------------------------------------------------------
```

If the unit tests have run successfully coverage file in LCOV format is
generated and stored at `coverage/lcov.info`. This file can be used by
your IDE to indicate code coverage from within your editor window.
- We recommend the Visual Studio Code extension
  [Code Coverage](https://marketplace.visualstudio.com/items?itemName=markis.code-coverage).
- Special care should be taken when modifying code that is not covered by unit tests!

Branches that do not pass the test harness (e.g. due to failing unit tests
or lowering the code coverage beneath the desired threshold) should not be
pull-requested.

### use the demo script

```SHELL
pdm run examples/demonstrator.py
pdm run examples/demonstrator.py -v -i 2
```
