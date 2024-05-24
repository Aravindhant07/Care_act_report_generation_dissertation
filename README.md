# Care Assessment Report Automation

## Introduction
This project automates the reporting requirements of the Care Act 2014 using a combination of IoT devices, advanced data processing, and AI-driven insights. The system, called Doris Pro, monitors the well-being of individuals under care, collecting data in real-time and generating detailed reports that provide valuable insights for care providers and regulatory bodies.

## Features
- **IoT Device Integration**: Utilizes Doris Pro devices for continuous monitoring of various health and environmental parameters.
- **Data Processing**: Employs Python for data cleaning, normalization, and analysis.
- **Insight Generation**: Integrates OpenAI's GPT models enhanced with Retrieval-Augmented Generation (RAG) to produce contextually rich and accurate reports.
- **Report Generation**: Uses LaTeX to generate professionally formatted reports.
- **Automated Email Distribution**: Automatically sends generated reports to stakeholders via email.

## Installation

### Prerequisites
- Python 3.8 or higher
- Required Python packages (listed in `requirements.txt`)
- LaTeX distribution (e.g., TeX Live, MiKTeX)
- Doris Pro IoT devices
- SMTP server credentials for email distribution

### Setup
1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/care-assessment-report.git
    cd care-assessment-report
    ```

2. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure environment variables**:
   - Create a `.env` file in the root directory and add the following:
     ```
     DETAILS_PATH=path/to/details.xlsx
     BASE_DATA_PATH=path/to/data/files
     IMAGE_DIR=path/to/save/images
     REPORT_DIR=path/to/save/reports
     HEADER_IMAGE=path/to/header_image.png
     FOOTER_IMAGE=path/to/footer_image.png
     SMTP_PASSWORD=your_smtp_password
     Directory=path/to/documents
     Log=path/to/logs
     OPENAI_API_KEY=your_openai_api_key
     ```

4. **Ensure the necessary directories exist**:
   ```bash
   mkdir -p path/to/save/images path/to/save/reports path/to/logs



## Project structure
```
care_assessment_report/
│
├── main.py
├── config/
│ └── config_loader.py
├── data/
│ └── data_loader.py
├── insights/
│ └── insights_generator.py
├── reporting/
│ └── report_generator.py
├── email/
│ └── email_sender.py
├── resources/
│ ├── header_image.png
│ └── footer_image.png
├── .env
└── requirements.txt
```

to run the script
```
python main.py
```
