#!/usr/bin/env python3
"""Sanity checks for the CV site. Builds the site first, so it can be run on its own.

The build goes to a temporary directory, so an existing or stale _site/ never affects the
result and is never modified.

Checks every CV data file (English and each translation) has the fields the templates rely
on, that the translations stay structurally in sync with the English file, and that each
built page is a single well-formed document whose internal links resolve.
"""
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is missing: run `pip install pyyaml`")

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA_FILES = {"cv.yml": "en", "cv_ar.yml": "ar"}
PAGES = {
    "index.html": "ltr",
    "ats-resume.html": "ltr",
    "ar/index.html": "rtl",
    "ar/ats-resume.html": "rtl",
}
errors = []


def load_data(name):
    try:
        cv = yaml.safe_load((ROOT / "_data" / name).read_text())
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"{name}: cannot be read as YAML: {exc}")
        return None
    if not isinstance(cv, dict):
        errors.append(f"{name}: top level must be a mapping")
        return None
    return cv


def check_data(name, cv):
    for key in ("personal", "summary", "skills", "experience", "education", "certifications"):
        if not cv.get(key):
            errors.append(f"{name}: missing or empty '{key}'")
    for key in ("name", "title"):
        if not cv.get("personal", {}).get(key):
            errors.append(f"{name}: personal.{key} is required")
    for skill in cv.get("skills") or []:
        if not skill.get("category") or not skill.get("items"):
            errors.append(f"{name}: skill entry needs 'category' and 'items': {skill}")
    for job in cv.get("experience") or []:
        for key in ("company", "position", "start_date", "end_date", "achievements"):
            if not job.get(key):
                errors.append(f"{name}: experience entry '{job.get('company')}' lacks '{key}'")
    for edu in cv.get("education") or []:
        for key in ("degree", "institution", "date"):
            if not edu.get(key):
                errors.append(f"{name}: education entry '{edu.get('degree')}' lacks '{key}'")
    for cert in cv.get("certifications") or []:
        for key in ("name", "issuer", "date"):
            if not cert.get(key):
                errors.append(f"{name}: certification '{cert.get('name')}' lacks '{key}'")


def check_translation(name, cv, base):
    """A translation must mirror cv.yml entry for entry: same counts, same identifiers, same links."""
    for key in ("skills", "experience", "education", "certifications", "languages", "projects"):
        a, b = len(base.get(key) or []), len(cv.get(key) or [])
        if a != b:
            errors.append(f"{name}: has {b} '{key}' entries, cv.yml has {a}")
    for i, (bj, j) in enumerate(zip(base.get("experience") or [], cv.get("experience") or [])):
        a, b = len(bj.get("achievements") or []), len(j.get("achievements") or [])
        if a != b:
            errors.append(f"{name}: experience #{i + 1} ('{j.get('company')}') has {b} achievements, cv.yml has {a}")
    for bs, s in zip(base.get("skills") or [], cv.get("skills") or []):
        a, b = len(bs["items"].split(", ")), len(s["items"].split(", "))
        if a != b:
            errors.append(f"{name}: skill category '{s.get('category')}' has {b} items, cv.yml has {a}")
    for bc, c in zip(base.get("certifications") or [], cv.get("certifications") or []):
        for key in ("id", "url"):
            if bc.get(key) != c.get(key):
                errors.append(f"{name}: certification '{c.get('name')}' {key} differs from cv.yml")
    for key in ("email", "phone", "linkedin", "github", "website"):
        if (base.get("personal") or {}).get(key) != (cv.get("personal") or {}).get(key):
            errors.append(f"{name}: personal.{key} differs from cv.yml")


def build_site(dest):
    if not shutil.which("bundle"):
        errors.append("bundle not found: install Ruby and run `bundle install`")
        return False
    result = subprocess.run(
        ["bundle", "exec", "jekyll", "build", "--destination", str(dest)],
        cwd=ROOT, capture_output=True, text=True,
    )
    if result.returncode != 0:
        errors.append("jekyll build failed:\n" + (result.stdout + result.stderr).strip())
        return False
    return True


def check_pages(site):
    for name, direction in PAGES.items():
        path = site / name
        if not path.is_file():
            errors.append(f"{name}: not built")
            continue
        html = path.read_text()
        for tag, expected in (("<!DOCTYPE", 1), ("<html", 1), ("<title>", 1), ("<body", 1)):
            found = html.count(tag)
            if found != expected:
                errors.append(f"{name}: expected {expected} '{tag}', found {found} (nested layout?)")
        if f'dir="{direction}"' not in html.split("<head>", 1)[0]:
            errors.append(f"{name}: <html> should declare dir=\"{direction}\"")
        if re.search(r"\{\{|\{%", html):
            errors.append(f"{name}: unrendered Liquid left in output")
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(("http", "mailto:", "#", "tel:")):
                continue
            # Absolute paths resolve from the site root, relative ones from the page's folder.
            if href.startswith("/"):
                target = site / href.lstrip("/")
            elif href == "./":
                target = path.parent
            else:
                target = (path.parent / href).resolve()
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{name}: internal link '{href}' does not resolve")
        for src in re.findall(r'(?:src|href)="(https?://[^"]+)"', html):
            if re.search(r"\.(css|js)(\?|$)", src):
                errors.append(f"{name}: loads external resource {src}; the pages are meant to be self-contained")


data = {name: load_data(name) for name in DATA_FILES}
for name, cv in data.items():
    if cv is not None:
        check_data(name, cv)
base = data.get("cv.yml")
if base is not None:
    for name, cv in data.items():
        if name != "cv.yml" and cv is not None:
            check_translation(name, cv, base)

if not errors:  # a broken data file would only make the build output noisy
    with tempfile.TemporaryDirectory(prefix="cv-site-") as tmp:
        if build_site(tmp):
            check_pages(pathlib.Path(tmp))

if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: {len(DATA_FILES)} data files valid and in sync, {len(PAGES)} pages well-formed, all internal links resolve")
