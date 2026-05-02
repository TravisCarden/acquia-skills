# Agent Skills

This directory contains Agent Skills that conform to the agentskills.io standard.

## Add a new skill

1. Create a new folder under `skills/` using a short, kebab-case name.
2. Add a `SKILL.md` file in that folder (the validator only picks up folders that contain `SKILL.md`).
3. Add the required manifest and any supporting files exactly as defined by the current agentskills.io specification.
4. Optional: include examples, tests, or assets referenced by your `SKILL.md`/manifest.

## Suggested layout

```
skills/
  my-skill/
    SKILL.md
    <manifest file per agentskills.io>
    <examples or assets>
```

## Validate locally

Use the official validator via the helper script:

```bash
python3 scripts/validate_manifests.py
```

## Reference

- Standard and schema: https://agentskills.io/
