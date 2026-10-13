# Contributing Guide

The `rs-embed` project welcomes bug reports, documentation fixes, model integrations, and API improvements. This page keeps the contribution workflow lightweight and points to the places where more detail already lives.

If you want to add a new model adapter or change the embedder contract, start with [Extending](extending.md).

## GitHub Workflow

All development happens on GitHub. If you already know what needs to change, the fastest path is usually to open a pull request. If the scope is still unclear, or if the change affects public API shape, model semantics, or repository direction, opening an issue first helps everyone start from the same written context.

For normal code contributions, fork the repository, create a focused branch, make the change, and open the pull request against `main`. Keeping unrelated changes in separate branches and PRs makes review much easier and usually gets feedback back to you faster.

```bash
git clone https://github.com/<your-username>/rs-embed.git
cd rs-embed
git checkout -b <descriptive-branch-name>
```

When you open the issue or PR, please include direct links to the relevant docs page, paper, model card, upstream repository, or prior discussion. If your claim depends on behavior, a plain-text code snippet is especially helpful because reviewers can search it, run it, and quote it directly.

## Issues

This repository includes GitHub issue forms for bug reports and feature requests. Please use them and include the links, code snippets, and environment details they ask for. That information usually answers the first round of clarifying questions before they need to be asked.

## Pull Requests

The repository also includes a pull request template. Please use it to summarize the change, link the related issue or reference material, and show how you verified the result. If the PR changes model behavior, it is especially helpful to mention the input contract, defaults, and any behavior that remains intentionally unsupported.

If a pull request changes public API, model defaults, output semantics, or user-facing installation behavior, please update `CHANGELOG.md` as part of the same change so the release record stays current.

Pull requests that touch user-facing or package-relevant files now get an automated changelog check in GitHub Actions. If a PR is intentionally docs-only, tests-only, CI-only, or otherwise internal, maintainers can apply the `skip-changelog` label to bypass that check.

## Tests

`rs-embed` uses GitHub Actions for continuous integration, and it helps a lot if pull requests keep those checks green. If you change Python behavior, please add or update tests so the new behavior is explicit and easy to review. The repository already contains many focused tests, so the easiest starting point is usually to find a nearby test and mirror its style rather than inventing a new pattern.

For a normal local setup, install the development dependencies first:

```bash
pip install -e ".[dev,full]"
```

Then run the checks that cover your change:

```bash
ruff check src/
ruff format src/ tests/
python -m pytest -v -n auto
```

If your change is local to one module or behavior, using a narrower pytest target is completely fine. Including that command in the pull request gives reviewers a concrete reproduction path instead of just a general statement that testing passed.

## Documentation

Documentation changes are real contributions, not just cleanup after the fact. If you change the public API, model semantics, installation story, or extension workflow, it helps a lot to update the docs while the implementation context is still fresh.

For doc changes, build the site locally before opening the pull request:

```bash
pip install mkdocs-material pymdown-extensions
mkdocs build --strict
```
