# Usage

## Running with Docker Compose

```bash
docker compose up --build
```

This starts the Grobid server and runs the pipeline automatically. To stop and clean up:

```bash
docker compose down
```

## Running Locally

A running [Grobid](https://github.com/kermitt2/grobid) server is required to process PDFs. You can run one locally with Docker:

```bash
docker run -d --rm -p 8070:8070 lfoppiano/grobid:0.8.1
```

Then update `config.json` with your server address if needed (defaults to `http://localhost:8070`).

```bash
python main.py
```

All paths and settings are read from `setup.cfg`:

```ini
[paths]
input = ./articles
grobid_output = ./grobid_output
results = ./prac_output

[grobid]
config = ./config.json
workers = 4
force = true
```

Edit `setup.cfg` to change input/output paths or Grobid settings.

## Pipeline Stages

1. **Grobid Processing** — sends PDFs from `articles/` to the Grobid server, outputs TEI-XML to `grobid_output/`
2. **XML Parsing** — extracts abstracts, figure counts, and links from the TEI-XML files
3. **Visualization** — generates word cloud and bar chart
4. **Links Export** — writes all links found per paper to a text file
