# Tool Integration Guide

How to load and use acquia-skills across different AI coding tools.

There are two ways to install skills:

- **Via skills.sh** (recommended) — one command installs skills directly into your tool when the package is published.
- **Manual installation** — copy skill files into the right location for your tool (useful during local development or before the package is published).

---

## Via skills.sh (Published Package)

When this package is published to [skills.sh](https://skills.sh), install skills with a single command using the `npx skills` CLI:

```bash
npx skills add acquia/acquia-skills
```

This automatically places the skill files in the correct location for your active AI tool.

### Tool-specific install commands

| Tool | Install command |
|---|---|
| Claude Code | `npx skills add acquia/acquia-skills` |
| GitHub Copilot (VS Code) | `npx skills add acquia/acquia-skills` |
| Cursor | `npx skills add acquia/acquia-skills` |
| Gemini CLI | `npx skills add acquia/acquia-skills` |
| OpenAI Codex | `npx skills add acquia/acquia-skills` |

The `npx skills` CLI detects the active tool and places files accordingly. See the [skills.sh documentation](https://skills.sh) for the full list of supported tools.

### Install individual skill sets

```bash
# acli skills only
npx skills add acquia/acquia-skills/skills/acli

# pipelines-cli skills only
npx skills add acquia/acquia-skills/skills/pipelines-cli

# drupal-maintenance skills only
npx skills add acquia/acquia-skills/skills/drupal-maintenance
```

### Keep skills up to date

```bash
npx skills update acquia/acquia-skills
```

---

## Manual Installation

Use this approach during local development or before the package is published to skills.sh.

### Claude Code

Skills go in `.claude/skills/` and are loaded automatically. Claude Code discovers and invokes them via the `Skill` tool based on description matching.

```bash
mkdir -p .claude/skills/acli .claude/skills/pipelines-cli .claude/skills/drupal-maintenance

# acli skills
cp /path/to/acquia-skills/skills/acli/*/SKILL.md .claude/skills/acli/

# pipelines-cli skills
cp /path/to/acquia-skills/skills/pipelines-cli/*/SKILL.md .claude/skills/pipelines-cli/

# drupal-maintenance skills
cp /path/to/acquia-skills/skills/drupal-maintenance/*/SKILL.md .claude/skills/drupal-maintenance/
```

To keep skills up to date:

```bash
git -C /path/to/acquia-skills pull
cp /path/to/acquia-skills/skills/acli/*/SKILL.md .claude/skills/acli/
cp /path/to/acquia-skills/skills/pipelines-cli/*/SKILL.md .claude/skills/pipelines-cli/
cp /path/to/acquia-skills/skills/drupal-maintenance/*/SKILL.md .claude/skills/drupal-maintenance/
```

---

### GitHub Copilot (VS Code)

Paste skill content into `.github/copilot-instructions.md` in your repo root. Copilot includes this file as context for every chat request in the workspace.

```bash
# Add a single skill
cat /path/to/acquia-skills/skills/acli/getting-started/SKILL.md >> .github/copilot-instructions.md

# Add all acli skills
for f in /path/to/acquia-skills/skills/acli/*/SKILL.md; do
  cat "$f" >> .github/copilot-instructions.md
  echo "" >> .github/copilot-instructions.md
done

# Add all drupal-maintenance skills
for f in /path/to/acquia-skills/skills/drupal-maintenance/*/SKILL.md; do
  cat "$f" >> .github/copilot-instructions.md
  echo "" >> .github/copilot-instructions.md
done
```

Only include skills relevant to the project to avoid overloading the context window.

---

### Cursor

Add skills as rule files under `.cursor/rules/`. Cursor loads `.mdc` files as individual rules and applies them based on relevance.

```bash
mkdir -p .cursor/rules

# Copy each skill as a separate rule file
for skill_dir in /path/to/acquia-skills/skills/acli/*/; do
  name=$(basename "$skill_dir")
  cp "$skill_dir/SKILL.md" ".cursor/rules/acli-${name}.mdc"
done

for skill_dir in /path/to/acquia-skills/skills/pipelines-cli/*/; do
  name=$(basename "$skill_dir")
  cp "$skill_dir/SKILL.md" ".cursor/rules/pipelines-cli-${name}.mdc"
done

for skill_dir in /path/to/acquia-skills/skills/drupal-maintenance/*/; do
  name=$(basename "$skill_dir")
  cp "$skill_dir/SKILL.md" ".cursor/rules/drupal-maintenance-${name}.mdc"
done
```

Alternatively, add a single combined rules file:

```bash
cat /path/to/acquia-skills/skills/acli/*/SKILL.md > .cursor/rules/acli.mdc
```

---

### Windsurf

Append skill content to `.windsurfrules` in your project root. Windsurf reads this file as persistent context for the Cascade AI.

```bash
# Add all acli skills
for f in /path/to/acquia-skills/skills/acli/*/SKILL.md; do
  cat "$f" >> .windsurfrules
  echo "" >> .windsurfrules
done

# Add drupal-maintenance skills
for f in /path/to/acquia-skills/skills/drupal-maintenance/*/SKILL.md; do
  cat "$f" >> .windsurfrules
  echo "" >> .windsurfrules
done
```

---

### Copilot CLI

Place skill files in the global skills directory. The Copilot CLI auto-discovers skills from installed plugins.

```bash
mkdir -p ~/.agents/skills/acli ~/.agents/skills/pipelines-cli ~/.agents/skills/drupal-maintenance

cp /path/to/acquia-skills/skills/acli/*/SKILL.md ~/.agents/skills/acli/
cp /path/to/acquia-skills/skills/pipelines-cli/*/SKILL.md ~/.agents/skills/pipelines-cli/
cp /path/to/acquia-skills/skills/drupal-maintenance/*/SKILL.md ~/.agents/skills/drupal-maintenance/
```

---

### Gemini CLI

Drop skill files into the Gemini skills directory and reference the product directories in `GEMINI.md`. Skills are activated via the `activate_skill` tool.

```bash
mkdir -p ~/.gemini/skills/acli ~/.gemini/skills/pipelines-cli ~/.gemini/skills/drupal-maintenance

cp /path/to/acquia-skills/skills/acli/*/SKILL.md ~/.gemini/skills/acli/
cp /path/to/acquia-skills/skills/pipelines-cli/*/SKILL.md ~/.gemini/skills/pipelines-cli/
cp /path/to/acquia-skills/skills/drupal-maintenance/*/SKILL.md ~/.gemini/skills/drupal-maintenance/
```

Add to `GEMINI.md` in your project:

```markdown
Skills are available in ~/.gemini/skills/. Use activate_skill to load acli or pipelines-cli skills when the user asks about those tools.
```

---

### General Rule

Any tool that supports custom instructions or a persistent context file (e.g., `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, system prompts) can use these skills by pasting the relevant `SKILL.md` content directly into that file.

The YAML frontmatter (`name`, `description`, `tags`) helps tools with semantic search surface the right skill at the right time — keep it intact when copying.

### What to include

| Use case | Recommended skills |
|---|---|
| Working with Acquia Cloud apps and environments | `acli-getting-started`, `acli-application-management`, `acli-environment-management` |
| Setting up a development environment | `acli-getting-started`, `acli-ide-management`, `acli-ssh-key-management` |
| Running CI/CD pipelines | `pipelines-cli-getting-started`, `pipelines-cli-pipeline-operations` |
| Scripting and automation | `acli-scripting`, `pipelines-cli-pipeline-operations` |
| Debugging issues | `acli-troubleshooting` |
| Fixing Drupal security vulnerabilities | `drupal-maintenance-security-updates` |
| Updating Drupal core or contrib packages | `drupal-maintenance-dependency-updates` |

See [`manifests/acli.yaml`](../manifests/acli.yaml), [`manifests/pipelines-cli.yaml`](../manifests/pipelines-cli.yaml), and [`manifests/drupal-maintenance.yaml`](../manifests/drupal-maintenance.yaml) for the full skill lists with IDs and paths.
