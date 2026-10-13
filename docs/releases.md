# Releases and Versioning

Earth Embedding is an independent derivative of the upstream package. Source
installation is the currently supported distribution route. PyPI publication
requires configuring a new trusted publisher for `GISWLH/earth-embedding`;
the workflow's publish jobs are disabled unless the repository variable
`EARTH_EMBEDDING_PYPI_ENABLED` is explicitly set to `true`.

This page defines the release policy for `earth-embedding`: where users should look for changes, how version numbers move, and which kinds of changes are treated as compatibility-sensitive.

---

## Source of Truth

`earth-embedding` keeps a repository-level [CHANGELOG](https://github.com/GISWLH/earth-embedding/blob/main/CHANGELOG.md) as the canonical release record.

GitHub Releases should mirror the matching changelog entry for each tagged version. This avoids a split workflow where the repository says one thing and the release page says another.

In practice:

1. Update `CHANGELOG.md`
2. Bump the package version
3. Run the manual TestPyPI publish workflow for the candidate version
4. Create a Git tag such as `v0.2.0`
5. Let the tag-triggered release workflow publish to PyPI and then create the GitHub Release from the matching `CHANGELOG.md` entry

---

## Versioning Policy

The project follows Semantic Versioning, but uses a stricter interpretation than a typical early-stage research package because users depend on stable API and embedding semantics.

### Patch Releases

Use `PATCH` for changes such as:

- bug fixes
- documentation-only improvements
- internal refactors that do not change public behavior
- packaging or CI fixes that do not affect runtime semantics

Example: `0.1.0` -> `0.1.1`

### Minor Releases

Use `MINOR` for backward-compatible feature work such as:

- adding a new model adapter
- adding a new public API that does not break existing callers
- adding new optional parameters with compatible defaults
- improving defaults without breaking existing results contracts

Example: `0.1.0` -> `0.2.0`

### Major Releases

Use `MAJOR` for breaking changes such as:

- removing or renaming a public API
- removing or renaming a public model ID
- changing a return type, output field, or shape contract
- changing the default semantics of an existing model in a way that can invalidate prior experiments

Example: `1.4.2` -> `2.0.0`

---

## Pre-1.0 Rule

The current package metadata still marks the library as alpha. Even so, breaking changes should not be hidden inside patch releases.

Before `1.0`, the project should treat compatibility conservatively:

- use `PATCH` only for safe fixes
- use `MINOR` when a change is user-visible, even if Python signatures stay the same
- clearly call out any migration work in the changelog and GitHub Release

This means `0.y.z` releases should already feel predictable to downstream users.

---

## What Counts as a Breaking Change Here

For a normal Python library, breakage is often just an import or signature issue. For `earth-embedding`, model behavior matters just as much as function signatures.

The following should be treated as compatibility-sensitive and called out explicitly:

- changing default preprocessing, normalization, or pooling for an existing model
- changing the default sensor, band order, temporal window interpretation, or compositing behavior
- changing the meaning or layout of `grid` or `pooled` outputs
- changing model-specific defaults in a way that can alter benchmark comparability
- removing a previously documented alias or adapter

If a user could rerun the same script and get embeddings with meaningfully different semantics, that change should be treated like a breaking API change even when the call signature looks identical.

---

## Release Checklist

For each package release:

1. Move notable changes from `Unreleased` into a dated version section in `CHANGELOG.md`
2. Bump [`src/rs_embed/_version.py`](https://github.com/GISWLH/earth-embedding/blob/main/src/rs_embed/_version.py)
3. Merge any required changelog updates before cutting the release tag
4. Run `release.yml` manually to publish the candidate build to TestPyPI
5. Confirm the TestPyPI smoke test can install, import, and invoke the `earth-embedding` CLI for `rs-embed==X.Y.Z`
6. Tag the release as `vX.Y.Z`
7. Let GitHub Actions publish the package to PyPI and then create the GitHub Release
8. If the change affects public behavior, update the relevant docs page and examples

---

## Package Publishing

`earth-embedding` publishes wheel and source distributions through PyPI Trusted Publishing, not long-lived API tokens.

Before the first package release:

1. Create separate owner accounts on [PyPI](https://pypi.org/) and [TestPyPI](https://test.pypi.org/).
2. In GitHub, create repository environments named `testpypi` and `pypi`.
3. Require manual approval on the `pypi` environment. The `testpypi` environment can stay unprotected.
4. In PyPI Trusted Publishers, register package name `earth-embedding` for repository `GISWLH/earth-embedding`, workflow file `release.yml`, and environment `pypi`.
5. In TestPyPI Trusted Publishers, register the same package and repository, but use environment `testpypi`.
6. Remove any old `PYPI_API_TOKEN` or `TEST_PYPI_API_TOKEN` repository secrets if earlier experiments used token-based uploads.

After that setup:

- `Actions -> release -> Run workflow` builds the current ref, uploads it to TestPyPI, and then runs a smoke test that installs the published package, imports `rs_embed`, and invokes `rs-embed --help`.
- Pushing a tag like `v0.2.0` runs the same build, checks that the tag matches `src/rs_embed/_version.py`, validates that `CHANGELOG.md` has a matching version section, publishes to PyPI, and only then creates the GitHub Release from the prevalidated release notes artifact.

For a local install check against TestPyPI, use:

```bash
python -m pip install \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple/ \
  rs-embed==X.Y.Z
```

Package versions on PyPI and TestPyPI are immutable. If a TestPyPI dry run exposed a packaging problem after upload, fix the issue and test again with a new version number rather than trying to overwrite the same release.

---

## Pull Request Enforcement

GitHub Actions checks pull requests for changelog coverage.

The check passes when any one of the following is true:

- `CHANGELOG.md` is updated in the PR
- the PR only touches docs, tests, CI, or other explicitly exempt internal files
- the PR has the `skip-changelog` label

This keeps the default behavior strict for public changes without forcing changelog edits for every maintenance-only PR.

---

## Where Users Should Look

- Repository changelog: [CHANGELOG.md](https://github.com/GISWLH/earth-embedding/blob/main/CHANGELOG.md)
- Package index: [PyPI](https://pypi.org/project/rs-embed/) and [TestPyPI](https://test.pypi.org/project/rs-embed/)
- Tagged releases: [GitHub Releases](https://github.com/GISWLH/earth-embedding/releases)
- Current package version: [`src/rs_embed/_version.py`](https://github.com/GISWLH/earth-embedding/blob/main/src/rs_embed/_version.py)
