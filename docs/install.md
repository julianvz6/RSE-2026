# Installation

## Option 1: Docker Compose (recommended)

The easiest way to run the pipeline — no manual setup of Grobid required:

```bash
git clone https://github.com/julianvz6/RSE-2026.git

docker compose up --build
```

This automatically starts the Grobid server, waits for it to be ready, and runs the pipeline. Results will appear in `prac_output/`.

**Requirements:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) must be installed and running.

## Option 2: Virtual Environment

### 1. Clone the repository

```bash
git clone https://github.com/julianvz6/RSE-2026.git
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv01
```

**Windows (PowerShell):**
```bash
.\venv01\Scripts\Activate.ps1
```

**Windows (CMD):**
```bash
.\venv01\Scripts\activate.bat
```

**Linux / macOS:**
```bash
source venv01/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start a Grobid server

A running [Grobid](https://github.com/kermitt2/grobid) server is required to process PDFs. You can run one locally with Docker:

```bash
docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.1
```

Then update `config.json` with your server address if needed (defaults to `http://localhost:8070`).

Pre-processed XML files are already included in `grobid_output/`, so this step is optional if you just want to run the analysis.
