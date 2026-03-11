# Individual Assessment 1 — PDF Article Analysis

[![DOI](https://zenodo.org/badge/1154798578.svg)](https://doi.org/10.5281/zenodo.18966270)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Automated pipeline that extracts structured data from academic PDF articles using [Grobid](https://github.com/kermitt2/grobid) and produces visualizations.

## Features

- **Keyword Cloud** — word cloud generated from all paper abstracts
- **Figures Chart** — bar chart showing the number of figures per article
- **Links List** — all external links found in each paper

## Quick Start

### Option A: Docker Compose (recommended)

```bash
git clone https://github.com/julianvz6/RSE-2026.git
docker compose up --build
```

### Option B: Local Python

```bash
git clone https://github.com/julianvz6/RSE-2026.git
python -m venv venv01
.\venv01\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
python main.py
```

See [Install](install.md) for full setup instructions and [Usage](usage.md) for details.
