# Markdown to HTML Static Site Generator

A small Python project that converts Markdown content into a complete static website.

## Main goal

Build a lightweight static site generator from scratch that:
- Parses Markdown files from `content/`
- Converts them to HTML pages
- Applies a shared `template.html`
- Copies static assets (CSS/images)
- Outputs a deployable site in `docs/`

## Project structure

- `src/` - generator logic (Markdown parsing, HTML node handling, page generation)
- `content/` - source Markdown pages/posts
- `static/` - static assets copied as-is
- `template.html` - page template used for all generated pages
- `docs/` - generated output (used for GitHub Pages deployment)
- `test/` - unit tests

## Scripts

There are 3 helper scripts in the project root:

- `main.sh` - generates the site and starts a local server on `http://localhost:8888`
- `build.sh` - generates production-ready output for GitHub Pages (correct base path)
- `test.sh` - runs the unit tests

## Quick start

```bash
./main.sh
```

For deployment build:

```bash
./build.sh
```

Optional custom base path:

```bash
GITHUB_PAGES_BASEPATH="/your-path/" ./build.sh
```

## Deployed version

GitHub Pages deployment (from `docs/`):  
`https://nasqnik.github.io/markdown_to_html/`