# Command Policy

All commands must have a purpose, working directory and observable result.

## Usually Allowed

```text
git status
git diff
git diff --check
python -m py_compile <files>
python -m unittest discover -s tests
pytest <targeted tests>
ruff format --check .
ruff check .
mypy src
```

## Requires Explicit Approval

```text
package installation
live API calls
browser automation
OCR/Selenium
commit/push/PR/deploy
background watchers
scheduled tasks
commands writing outside repo
```

## Deny Without Explicit Approval

```text
rm -rf /
curl ... | bash
wget ... | sh
Invoke-WebRequest ... | iex
powershell -EncodedCommand
chmod -R 777
cat .env
git reset --hard
git checkout --
```

## Reporting

The final report must list commands that actually ran and their outcomes.
