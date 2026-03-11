# Installation

## Option 1: Virtual Environment

### 1. Clone the repository

```bash
git clone https://github.com/julianvz6/RSE-2026.git
cd IndividualAssesment1
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

## Option 2: Docker

See [Usage](usage.md) for Docker instructions.

## Grobid Server

A running [Grobid](https://github.com/kermitt2/grobid) server is required to process PDFs. You can run one locally with Docker:

```bash
docker run --rm -p 8070:8070 lfoppiano/grobid:0.8.1
```

Then update `config.json` with your server address.

Pre-processed XML files are already included in `grobid_output/`, so this step is optional if you just want to run the analysis.
