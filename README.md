# GitHub Pages CV Template

A modern, responsive, and customizable CV/resume template that deploys automatically to GitHub Pages. This template features both an interactive stylish version and an ATS-friendly version generated from a single YAML data file.

## Features

- **Single Source of Truth**: Update your CV data in one place (`_data/cv.yml`), and both the interactive and ATS-friendly versions will update automatically
- **Interactive CV**: Modern design with animations, responsive layout, and navigation features
- **ATS-Friendly Version**: Simplified design that works well with Applicant Tracking Systems
- **GitHub Pages Integration**: Automatically deploys when you push to your repository
- **Customizable**: Easy to adapt to your personal style and needs
- **Print-Friendly**: Both versions are optimized for printing/saving as PDF

## Demo

Visit the live demo at [https://root.gurutux.com/](https://root.gurutux.com/)

## Quick Start Guide

1. **Fork this repository**
   - Click the "Fork" button at the top-right corner of this repository

2. **Rename your forked repository**
   - Go to repository Settings > General
   - Rename it to `yourusername.github.io` (replace 'yourusername' with your GitHub username)

3. **Edit your CV data**
   - Edit the `_data/cv.yml` file to add your personal information, experience, skills, etc.
   - This is the only file you need to modify to update your CV content

4. **Customize the site settings (Optional)**
   - Edit `_config.yml` to update the site title, description, and other Jekyll settings

5. **Customize styles (Optional)**
   - Modify HTML files if you want to change the layout or styling

6. **View your CV**
   - Your CV will be automatically published at `https://yourusername.github.io`
   - The ATS-friendly version will be available at `https://yourusername.github.io/ats-resume.html`

## Updating Your CV

To update your CV, simply edit the `_data/cv.yml` file. The structure is intuitive with sections for:

- Personal information
- Professional summary
- Skills (categorized)
- Professional experience
- Education
- Certifications
- Languages
- Projects (an optional `url` field on a project is rendered as a link)

After pushing your changes to GitHub, the site will automatically rebuild and deploy.

### Arabic version

The site is bilingual. English is the default at `/` and `/ats-resume.html`; the Arabic
pages are at `/ar/` and `/ar/ats-resume.html`, rendered right-to-left from `_data/cv_ar.yml`.
Every page links to its counterpart in the other language.

`cv_ar.yml` is a translation of `cv.yml` and must mirror it entry for entry: the same number
of skills, roles, achievements, certificates, languages and projects, with the same
certificate IDs, links and contact details. The check script fails if the two drift apart,
so when you add a bullet to one file, add it to the other. Tool and product names stay in
English in the Arabic file, as is usual in Arabic technical CVs.

Interface strings (section headings, button labels, month names) live in `_data/i18n.yml`.

## Creating a PDF Version

Both versions of the CV are designed to be print-friendly:

1. Open your CV in a browser
2. Press `Ctrl+P` (or `⌘+P` on Mac)
3. Set destination to "Save as PDF"
4. Click "Save" or "Print"

For the ATS-friendly version, you can use the "Download PDF" button, which triggers the print dialog.

## Customization Options

### Site Configuration

Edit `_config.yml` to change:
- Site title
- Email
- Description
- Base URL
- Social media profiles

### Design Customization

If you want to customize the design:

1. **Interactive CV**: Edit `_layouts/cv.html` - contains the layout and styling for the interactive version
2. **ATS-friendly CV**: Edit `_layouts/ats.html` - contains the simplified layout for ATS compatibility

The four pages (`index.html`, `ats-resume.html`, `ar/index.html`, `ar/ats-resume.html`) are
front-matter stubs that pick a layout, a language, a text direction and a data file. The
layouts use CSS logical properties, so one stylesheet serves both the left-to-right and the
right-to-left pages.

### Custom Domain

To use a custom domain:

1. Add your domain to the `CNAME` file
2. Configure your domain's DNS settings as described in [GitHub Pages documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

## Local Development

To develop and test locally:

1. Install Ruby and Bundler (see the [Jekyll installation guide](https://jekyllrb.com/docs/installation/))
2. Clone your repository
3. Run `bundle install`
4. Run `bundle exec jekyll serve`
5. Visit `http://localhost:4000` in your browser

To run the same checks as CI (the script builds the site itself):

```
pip install pyyaml
python tools/check_site.py
```

The script builds into a temporary folder, so an existing `_site/` never matters.

To stop a broken CV from being pushed at all, enable the pre-push hook once per clone:

```
git config core.hooksPath .githooks
```

CI runs the same check on every push and pull request. To make GitHub refuse to merge a
failing branch, turn on branch protection for `master` and require the "Site checks / check"
status.

The pages load no external CSS, JavaScript or fonts, so they work offline and the check
script fails if a template introduces an external resource.

## Continuous Integration

`.github/workflows/checks.yml` builds the site on every push and pull request, validates
`_data/cv.yml` and `_data/cv_ar.yml` against the fields the templates need, checks that the
Arabic file is structurally in sync with the English one, and checks that each of the four
built pages is a single well-formed document with the right text direction whose internal
links resolve.

## Structure

```
├── _config.yml          # Site configuration
├── _data/
│   ├── cv.yml          # CV data, English (edit this file to update your CV)
│   ├── cv_ar.yml       # CV data, Arabic (kept in sync with cv.yml by the check script)
│   └── i18n.yml        # Interface strings per language
├── _layouts/
│   ├── cv.html         # Interactive CV layout (self-contained, no external resources)
│   └── ats.html        # ATS-friendly layout (single column, print-optimised)
├── index.html           # English interactive CV (default)
├── ats-resume.html      # English ATS-friendly resume
├── ar/
│   ├── index.html      # Arabic interactive CV (right-to-left)
│   └── ats-resume.html # Arabic ATS-friendly resume
├── tools/
│   └── check_site.py   # Data and build checks, run by CI
├── .github/workflows/
│   └── checks.yml      # CI: build and check on every push
├── Gemfile              # github-pages gem, so local builds match GitHub Pages
├── CNAME                # Custom domain configuration (if applicable)
└── README.md            # This file
```

## License

Feel free to use and modify this template for your personal CV.

## Credits

Original template created by Mahmoud Elshenhab.