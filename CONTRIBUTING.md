# Contributing to Acquia Skills

Thank you for your interest in this project!

## Reporting Issues

Feature requests, bugs, and support requests are tracked via the [GitHub issue queue](https://github.com/acquia/acquia-skills/issues) and are open to everyone. Before submitting an issue, please read and take the time to understand this guide. Issues not adhering to these guidelines may be closed.

- Issues filed with this project are not subject to an SLA.
- Acquia Skills is distributed under the MIT license; all documentation, code, and guidance is provided without warranty.
- The project maintainers are under no obligation to respond to support requests, feature requests, or pull requests.

## Contribution Policy

**This repository is publicly visible but contributions are restricted.**

Project maintainers can follow the guidelines below.

## Getting Started

1. Clone the repository and create a branch from `main`.
2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
3. Make your changes following the conventions described below.

## Adding or Updating Skills

- Skills live under `skills/<toolkit>/<skill-name>/SKILL.md`.
- Each skill must have a corresponding entry in the manifest at `manifests/<toolkit>.yaml`.
- Manifest `name` must match the skill's directory name exactly.

Validate your changes before opening a PR:

```bash
python3 scripts/validate_manifests.py
```

To auto-fix a `name` field mismatch:

```bash
python3 scripts/validate_manifests.py --fix
```

## Pull Request Guidelines

- **Branch naming**: use a descriptive name such as `add-<skill-name>` or `fix-<skill-name>`.
- **PR title**: short, imperative sentence (e.g. `Add security-updates skill for pipelines-cli`).
- Keep changes focused — one skill or fix per PR.
- Update the `README.md` skills table if you add a new skill.

