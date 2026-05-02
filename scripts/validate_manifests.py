import sys
import os
import re
import yaml

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

REQUIRED_INDEX_FIELDS = {"id", "product", "audience", "path"}
PATH_PATTERN = re.compile(r"^skills/([^/]+)/[^/]+/SKILL\.md$")
NAME_VALID = re.compile(r"^[a-z0-9-]+$")


def validate_schema(skills, valid_products):
    id_pattern = re.compile(r"^(" + "|".join(re.escape(p) for p in valid_products) + r")-[a-z0-9][a-z0-9-]*$")
    errors = []
    seen_ids = {}
    for skill in skills:
        skill_id = skill.get("id") or "<missing id>"
        for field in REQUIRED_INDEX_FIELDS:
            if not skill.get(field):
                errors.append(f"{skill_id}: missing required field '{field}'")
        if skill.get("audience") and skill.get("audience") != "user":
            errors.append(f"{skill_id}: audience must be 'user', got '{skill.get('audience')}'")
        if skill.get("product") and skill.get("product") not in valid_products:
            errors.append(f"{skill_id}: product must be one of {sorted(valid_products)}, got '{skill.get('product')}'")
        path = skill.get("path", "")
        if path:
            match = PATH_PATTERN.match(path)
            if not match:
                errors.append(f"{skill_id}: path does not match skills/<product>/<skill-name>/SKILL.md: {path}")
            elif match.group(1) != skill.get("product"):
                errors.append(f"{skill_id}: path product '{match.group(1)}' does not match product field '{skill.get('product')}'")
        if skill_id in seen_ids:
            errors.append(f"Duplicate ID: {skill_id}")
        else:
            seen_ids[skill_id] = True
        if skill_id != "<missing id>" and not id_pattern.match(skill_id):
            errors.append(f"{skill_id}: ID must match <product>-<skill-name> pattern (e.g. acli-ide-management)")
    return errors


def validate_paths(skills):
    errors = []
    for skill in skills:
        path = skill.get("path", "")
        if path:
            full = path if os.path.isabs(path) else os.path.join(_REPO_ROOT, path)
            if not os.path.exists(full):
                errors.append(f"{skill.get('id', '<missing>')}: path does not exist: {path}")
    return errors


def validate_skill_file(path):
    """Validate a SKILL.md file against the agentskills.io spec."""
    errors = []
    try:
        with open(path) as f:
            content = f.read()
        if not content.startswith("---"):
            errors.append(f"{path}: no frontmatter found (file must start with ---)")
            return errors
        try:
            end = content.index("---", 3)
        except ValueError:
            errors.append(f"{path}: frontmatter is not closed (missing closing ---)")
            return errors
        fm = yaml.safe_load(content[3:end]) or {}

        name = fm.get("name", "")
        description = fm.get("description", "")

        # name: required
        if not name:
            errors.append(f"{path}: missing frontmatter field 'name'")
        else:
            # name: max 64 chars
            if len(name) > 64:
                errors.append(f"{path}: name exceeds 64 characters: '{name}'")
            # name: only lowercase letters, numbers, hyphens
            if not NAME_VALID.match(name):
                errors.append(f"{path}: name '{name}' contains invalid characters — only lowercase letters, numbers, and hyphens allowed")
            # name: no leading hyphen
            if name.startswith("-"):
                errors.append(f"{path}: name '{name}' must not start or end with a hyphen")
            # name: no trailing hyphen
            if name.endswith("-"):
                errors.append(f"{path}: name '{name}' must not start or end with a hyphen")
            # name: no consecutive hyphens
            if "--" in name:
                errors.append(f"{path}: name '{name}' must not contain consecutive hyphens")
            # name: must match parent directory name (agentskills.io spec)
            dir_name = os.path.basename(os.path.dirname(os.path.abspath(path)))
            if name != dir_name:
                errors.append(
                    f"{path}: name '{name}' does not match parent directory '{dir_name}' "
                    f"(agentskills.io spec requires name == directory name)"
                )

        # description: required, max 1024 chars
        if not description:
            errors.append(f"{path}: missing frontmatter field 'description'")
        elif len(description) > 1024:
            errors.append(f"{path}: description exceeds 1024 characters ({len(description)} chars)")

        # compatibility: optional, max 500 chars
        compatibility = fm.get("compatibility", "")
        if compatibility and len(str(compatibility)) > 500:
            errors.append(f"{path}: compatibility exceeds 500 characters ({len(str(compatibility))} chars)")

    except Exception as e:
        errors.append(f"{path}: could not parse: {e}")
    return errors


def fix_skill_file(path):
    """Fix name field in SKILL.md to match parent directory name. Returns True if changed, False if already correct."""
    try:
        with open(path) as f:
            content = f.read()
        if not content.startswith("---"):
            return False
        try:
            end = content.index("---", 3)
        except ValueError:
            return False
        fm_str = content[3:end]
        fm = yaml.safe_load(fm_str) or {}
        dir_name = os.path.basename(os.path.dirname(os.path.abspath(path)))
        if fm.get("name") == dir_name:
            return False
        new_fm_str = re.sub(r"^name:.*$", f"name: {dir_name}", fm_str, flags=re.MULTILINE)
        new_content = "---" + new_fm_str + "---" + content[end + 3:]
        with open(path, "w") as f:
            f.write(new_content)
        return True
    except OSError as e:
        print(f"ERROR: could not fix {path}: {e}", file=sys.stderr)
        return False


def load_index(path=None):
    if path is None:
        path = os.path.join(_REPO_ROOT, "manifests", "skills-index.yaml")
    with open(path) as f:
        return yaml.safe_load(f)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Validate skills-index.yaml and SKILL.md files")
    parser.add_argument("--fix", action="store_true", help="Auto-fix name mismatches in SKILL.md files")
    args = parser.parse_args()

    index = load_index()
    skills = index.get("skills", [])
    valid_products = {p["id"] for p in index.get("products", [])}
    errors = validate_schema(skills, valid_products)
    errors += validate_paths(skills)

    for skill in skills:
        path = skill.get("path", "")
        if not (path and os.path.exists(path)):
            continue
        if args.fix:
            if fix_skill_file(path):
                print(f"FIXED: {path}")
        errors += validate_skill_file(path)

    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
    print(f"OK: {len(skills)} skills validated")


if __name__ == "__main__":
    main()
