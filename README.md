# Acquia Skills

Agent Skills for [Acquia CLI](https://docs.acquia.com/acquia-cli/), [Pipelines CLI](https://docs.acquia.com/acquia-cloud-platform/pipelines/), Drupal dependency management, and end-to-end deployment playbooks. Compatible with Claude Code, GitHub Copilot, Cursor, Gemini CLI, and any tool that supports the [agentskills.io](https://agentskills.io) format.

## Skills

### `acli` — Acquia CLI

| Skill | Description |
|-------|-------------|
| `getting-started` | Install and authenticate acli for the first time |
| `application-management` | List applications, link repos, check VCS status |
| `environment-management` | List, create, delete, and mirror Cloud environments |
| `ide-management` | Create, list, open, and manage Cloud IDEs |
| `pull-push` | Sync code, database, and files between local and Cloud |
| `remote-access` | SSH into environments, run Drush remotely, tail logs |
| `ssh-key-management` | Add, list, and delete SSH keys |
| `codestudio` | Set up Code Studio (GitLab CI/CD) projects |
| `scripting` | Run acli non-interactively in scripts and CI/CD |
| `troubleshooting` | Debug acli errors and authentication failures |

### `pipelines-cli` — Acquia Pipelines CLI

| Skill | Description |
|-------|-------------|
| `getting-started` | Install and authenticate the Pipelines CLI |
| `application-management` | Find application IDs and link repos |
| `pipeline-operations` | Trigger builds, check status, stream logs, terminate jobs |

### `drupal-maintenance` — Drupal Dependency Management

| Skill | Description |
|-------|-------------|
| `security-updates` | Audit and fix vulnerable packages using Composer |
| `dependency-updates` | Update outdated packages, Drupal core, and contrib modules |

### `playbooks` — End-to-End Workflows

| Skill | Description |
|-------|-------------|
| `drupal-update-deploy` | Update Drupal dependencies, push code, deploy to environment, and optionally trigger a pipeline |

## Installation

See [docs/tool-integration.md](docs/tool-integration.md) for tool-specific installation instructions (Claude Code, GitHub Copilot, Cursor, Gemini CLI, and more).

## Validation

Before publishing new or updated skills, run:

```bash
python3 scripts/validate_manifests.py
```

To auto-fix a `name` field that doesn't match its directory name:

```bash
python3 scripts/validate_manifests.py --fix
```

The script checks every `SKILL.md` against the [agentskills.io spec](https://agentskills.io/specification) and validates all entries in `manifests/skills-index.yaml`.

### Adding a new skill

1. Create a directory under `skills/<product>/<skill-name>/`
2. Add a `SKILL.md` with `name` matching the directory name
3. Add an entry to `manifests/skills-index.yaml`
4. Run `python3 scripts/validate_manifests.py` — fix any errors before publishing
