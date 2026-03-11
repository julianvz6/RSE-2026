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
.\venv01\Scripts\activate
```

**Windows (CMD):**
```bash
.\venv01\Scripts\activate
```

**Linux / macOS:**
```bash
source venv01/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```
