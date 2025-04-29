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
- Projects

After pushing your changes to GitHub, the site will automatically rebuild and deploy.

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

1. **Interactive CV**: Edit `index.html` - contains the layout and styling for the interactive version
2. **ATS-friendly CV**: Edit `ats-resume.html` - contains the simplified layout for ATS compatibility

### Custom Domain

To use a custom domain:

1. Add your domain to the `CNAME` file
2. Configure your domain's DNS settings as described in [GitHub Pages documentation](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site)

## Local Development

To develop and test locally:

1. Install [Jekyll](https://jekyllrb.com/docs/installation/)
2. Clone your repository
3. Run `bundle install`
4. Run `bundle exec jekyll serve`
5. Visit `http://localhost:4000` in your browser

## Structure

```
├── _config.yml          # Site configuration
├── _data/
│   └── cv.yml          # CV data (edit this file to update your CV)
├── index.html           # Interactive CV template
├── ats-resume.html      # ATS-friendly CV template
├── CNAME                # Custom domain configuration (if applicable)
└── README.md            # This file
```

## License

Feel free to use and modify this template for your personal CV.

## Credits

Original template created by Mahmoud Elshenhab.