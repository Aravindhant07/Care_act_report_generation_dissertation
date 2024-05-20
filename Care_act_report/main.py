from config.config import ConfigLoader
from data.data_loader import DataLoader
from insights.insights_generator import InsightGenerator
from reporting.report_generator import ReportGenerator
from emailsend.email_sender import EmailSender
import logging

def main():
    # Load configuration
    config = ConfigLoader().load_config()

    # Setup logging
    logging.basicConfig(filename=config['log_file'], level=logging.INFO)

    # Load and validate the details file
    try:
        details_df = DataLoader(config).load_details()
    except Exception as e:
        logging.error(f"Failed to read details file: {e}")
        return

    # Initialize necessary components
    insight_generator = InsightGenerator(config)
    report_generator = ReportGenerator(config)
    email_sender = EmailSender(config)

    for index, row in details_df.iterrows():
        name, email = row['Name'], row['Email']
        file_path = f"{config['base_data_path']}/{row['File name']}.xlsx"

        try:
            # Load and preprocess data
            df = DataLoader(config).load_and_prepare_data(file_path)

            # Generate insights
            insights = insight_generator.generate_insights(df)

            # Plot graphs
            filename_base = f"{config['image_dir']}/{name}"
            report_generator.plot_graphs(df, filename_base)

            # Generate LaTeX report
            tex_file_path = report_generator.generate_latex_report(name, insights, filename_base)

            # Compile LaTeX to PDF
            pdf_path = report_generator.compile_latex_to_pdf(tex_file_path)

            # Send email
            if pdf_path:
                email_sender.send_email(pdf_path, email, f"{name}_Care_Assessment_Report.pdf", "Please find attached the Care Assessment Report.")
            else:
                logging.error(f"Failed to compile LaTeX to PDF for {name}. Email not sent.")
        except Exception as e:
            logging.error(f"Failed to process data for {name}: {e}")

if __name__ == "__main__":
    main()
