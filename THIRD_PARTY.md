# Bundled Markdown parser

`vendor/` contains unmodified, pinned packages installed from official PyPI releases:

- [markdown-it-py 3.0.0](https://pypi.org/project/markdown-it-py/3.0.0/) — MIT License.
- [mdurl 0.1.2](https://pypi.org/project/mdurl/0.1.2/) — MIT License.

Their distribution metadata and license files are included. These versions support the project's Python 3.9 baseline. No package installation or network access is needed during ordinary builds. To refresh, install reviewed versions into an empty `vendor/` directory with `--no-compile --no-deps` and run the checks.

Markdown is parsed with raw HTML disabled, following the parser's [security guidance](https://markdown-it-py.readthedocs.io/en/latest/security.html). Uploaded Markdown supplies content, not executable HTML or scripts.
