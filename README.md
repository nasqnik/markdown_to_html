# Markdown to HTML Static Site Generator

A Python project that converts Markdown content into a complete static website and deploys it with GitHub Pages.

## Main goal

Build a lightweight static site generator from scratch with a clean parsing/rendering pipeline, reproducible scripts, and deployable output.

## Features

- Converts Markdown files in `content/` into HTML pages
- Supports headings, paragraphs, bold/italic text, code blocks, lists, links, and images
- Applies shared layout using `template.html`
- Copies static assets (CSS/images) into the output
- Generates production-ready output in `docs/` for GitHub Pages

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
./test.sh
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

## Architecture (high level)

- **Markdown parser**: turns markdown blocks/inline text into internal node structures
- **HTML generation**: converts node trees into HTML fragments
- **Page renderer**: injects title/content into `template.html`
- **Static copier**: copies files from `static/` to `docs/`

## Technical notes

- Separates parsing from rendering to keep the code easier to test
- Handles GitHub Pages path prefixing during build
- Uses unit tests in `test/` to validate parser and node behavior

## Limitations / next steps

- Not a full CommonMark implementation
- No front matter metadata yet
- No plugin system or incremental builds yet

## Deployed version

GitHub Pages deployment (from `docs/`):  
`https://nasqnik.github.io/markdown_to_html/`

![Project demo](./static/demo.gif)