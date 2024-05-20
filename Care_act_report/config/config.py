import os
from dotenv import load_dotenv

class ConfigLoader:
    def load_config(self):
        load_dotenv()
        return {
            'details_path': os.getenv('DETAILS_PATH'),
            'base_data_path': os.getenv('BASE_DATA_PATH'),
            'image_dir': os.getenv('IMAGE_DIR'),
            'report_dir': os.getenv('REPORT_DIR'),
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'smtp_user': 'aravindhant7@gmail.com',
            'smtp_password': os.getenv('SMTP_PASSWORD'),
            'header_image': os.getenv('HEADER_IMAGE'),
            'footer_image': os.getenv('FOOTER_IMAGE'),
            'report_timeframe': 'quarterly',
            'Directory': os.getenv('Directory'),
            'log_dir': os.getenv('Log'),
            'log_file': os.path.join(os.getenv('Log'), "care_assessment_report.log")
        }
