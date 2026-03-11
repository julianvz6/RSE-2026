# Prac1-RSE

Automated pipeline that extracts structured data from academic PDF articles using [Grobid](https://github.com/kermitt2/grobid) and produces visualizations.

## Features

- **Keyword Cloud** — word cloud generated from all paper abstracts
- **Figures Chart** — bar chart showing the number of figures per article
- **Links List** — all external links found in each paper

## Quick Start

```bash
git clone https://github.com/julianvz6/RSE-2026.git
cd IndividualAssesment1
python -m venv venv01
.\venv01\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
python main.py
```

See [Install](install.md) for full setup instructions and [Usage](usage.md) for details.
