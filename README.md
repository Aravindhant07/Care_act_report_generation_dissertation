# Care Assessment Report Automation

MSc Data Science dissertation project (University of Roehampton, 2024).

Automates the well-being reporting required under the **UK Care Act 2014**. Sensor data from *Doris Pro* IoT devices is turned into a personalised PDF care-assessment report for each person, with AI-written insights, and emailed to the right contact. No manual work is needed.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![LangChain](https://img.shields.io/badge/LangChain-RAG-green) ![OpenAI](https://img.shields.io/badge/OpenAI-GPT--3.5-412991) ![LaTeX](https://img.shields.io/badge/Reports-LaTeX-008080)

## How it works

```
Frailty score data (.xlsx)
        │
        ▼
 DataLoader ──► clean & normalise readings per well-being domain
        │       (nutrition, hygiene, toilet needs, safe home, relationships ...)
        ▼
 InsightGenerator ──► RAG pipeline: Chroma vector store of Care Act guidance
        │             + GPT-3.5 → empathetic, score-aware insights per domain
        ▼
 ReportGenerator ──► trend charts (seaborn) + LaTeX → PDF report
        ▼
 EmailSender ──► SMTP delivery to each person's contact
```

## Features

- **IoT data ingestion:** reads time-stamped scores for nine Care Act well-being domains.
- **Retrieval-Augmented Generation:** grounds GPT output in reference documents, so the insights stay on topic and cite the actual scores.
- **Professional reports:** a LaTeX template with header and footer branding, plus a chart for each domain and an overall trend chart.
- **Automated distribution:** each report is emailed to the address listed for that person in `Details.xlsx`.

## Project structure

```
Care_act_report/
├── main.py                     # Orchestrates the pipeline for every person
├── config/config.py            # Loads settings from environment variables (.env)
├── data/data_loader.py         # Reads and prepares the Excel data
├── insights/insights_generator.py  # LangChain + Chroma RAG insights
├── reporting/report_generator.py   # Charts + LaTeX/PDF report
├── emailsend/email_sender.py   # SMTP email delivery
├── Frailty score data/         # Sample sensor data for testing
├── Details.xlsx                # Person → data file → email mapping (sample)
├── Retrival_data/              # Reference documents for the RAG store
├── resources/                  # Report header/footer images
└── requirements.txt
```

## Getting started

### Prerequisites
- Python 3.8+
- A LaTeX distribution (TeX Live or MiKTeX) with `pdflatex` on your PATH
- An OpenAI API key
- An SMTP account for sending email (for Gmail, use an [App Password](https://support.google.com/accounts/answer/185833))

### Setup

```bash
git clone https://github.com/Aravindhant07/Care_act_report_generation_dissertation.git
cd Care_act_report_generation_dissertation/Care_act_report
pip install -r requirements.txt
```

Create a `.env` file in `Care_act_report/`. It is git-ignored, so keep secrets here only:

```ini
OPENAI_API_KEY=your_openai_api_key
SMTP_USER=you@example.com
SMTP_PASSWORD=your_app_password
DETAILS_PATH=Details.xlsx
BASE_DATA_PATH=Frailty score data
Directory=Retrival_data
IMAGE_DIR=images
REPORT_DIR=report
HEADER_IMAGE=resources/header.png
FOOTER_IMAGE=resources/footer.png
Log=logs
```

```bash
mkdir -p images report logs
python main.py
```

The Chroma vector store (`db/`) is rebuilt automatically on each run.

> **Note:** ChromaDB needs SQLite 3.35 or newer. If your system's SQLite is older, run `pip install pysqlite3-binary`.

## Tech stack

Python · pandas · seaborn/matplotlib · LangChain · ChromaDB · OpenAI GPT-3.5 · PyLaTeX · SMTP

## Data

The files in `Frailty score data/` are sample data for testing. The email addresses in `Details.xlsx` are placeholders.

## License

[Mozilla Public License 2.0](LICENSE)
