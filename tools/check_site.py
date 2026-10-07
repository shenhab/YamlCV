#!/usr/bin/env python3
"""Sanity checks for the CV site. Run after `bundle exec jekyll build`.

Checks the data file has every field the templates rely on, and that each built page
is a single well-formed document whose internal links resolve.
"""
import pathlib
import re
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "_site"
PAGES = ["index.html", "ats-resume.html"]
errors = []


def check_data():
    cv = yaml.safe_load((ROOT / "_data" / "cv.yml").read_text())
    for key in ("personal", "summary", "skills", "experience", "education", "certifications"):
        if not cv.get(key):
            errors.append(f"cv.yml: missing or empty '{key}'")
    for key in ("name", "title"):
        if not cv.get("personal", {}).get(key):
            errors.append(f"cv.yml: personal.{key} is required")
    for skill in cv.get("skills") or []:
        if not skill.get("category") or not skill.get("items"):
            errors.append(f"cv.yml: skill entry needs 'category' and 'items': {skill}")
    for job in cv.get("experience") or []:
        for key in ("company", "position", "start_date", "end_date", "achievements"):
            if not job.get(key):
                errors.append(f"cv.yml: experience entry '{job.get('company')}' lacks '{key}'")
    for cert in cv.get("certifications") or []:
        for key in ("name", "issuer", "date"):
            if not cert.get(key):
                errors.append(f"cv.yml: certification '{cert.get('name')}' lacks '{key}'")


def check_pages():
    if not SITE.is_dir():
        errors.append("_site/ not found: run `bundle exec jekyll build` first")
        return
    for name in PAGES:
        path = SITE / name
        if not path.is_file():
            errors.append(f"{name}: not built")
            continue
        html = path.read_text()
        for tag, expected in (("<!DOCTYPE", 1), ("<html", 1), ("<title>", 1), ("<body", 1)):
            found = html.count(tag)
            if found != expected:
                errors.append(f"{name}: expected {expected} '{tag}', found {found} (nested layout?)")
        if re.search(r"\{\{|\{%", html):
            errors.append(f"{name}: unrendered Liquid left in output")
        for href in re.findall(r'href="([^"]+)"', html):
            if href.startswith(("http", "mailto:", "#", "tel:")):
                continue
            target = (SITE / href.lstrip("/")) if href != "./" else SITE / "index.html"
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{name}: internal link '{href}' does not resolve")
        for src in re.findall(r'(?:src|href)="(https?://[^"]+)"', html):
            if re.search(r"\.(css|js)(\?|$)", src):
                errors.append(f"{name}: loads external resource {src}; the pages are meant to be self-contained")


check_data()
check_pages()
if errors:
    print("\n".join(errors))
    sys.exit(1)
print(f"OK: data file valid, {len(PAGES)} pages well-formed, all internal links resolve")
