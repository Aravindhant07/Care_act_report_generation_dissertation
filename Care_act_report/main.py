import os
from config.config import Config
from data.data_loader import DataLoader
from insights.insights_generator import InsightsGenerator
from reporting.report_generator import ReportGenerator
from emailsend.email_sender import EmailSender
from utils.logging_setup import setup_logging
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI

# Ensure necessary directories exist
Config.ensure_directories()

# Setup logging
setup_logging(Config.LOG_DIR)

# Load documents and setup retriever
def load_docs(directory):
    """Load documents from a specified directory using a DirectoryLoader."""
    loader = DirectoryLoader(directory, show_progress=True)
    documents = loader.load()
    return documents

documents = load_docs(Config.DIRECTORY)

def split_docs(documents, chunk_size=1000, chunk_overlap=100):
    """Split documents into smaller chunks for processing."""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    docs = text_splitter.split_documents(documents)
    return docs

docs = split_docs(documents)

# Initialize OpenAI embeddings
embeddings = OpenAIEmbeddings(openai_api_key=os.environ["OPENAI_API_KEY"])

# Embed and store the texts, using Chroma for vector storage and retrieval
persist_directory = 'db'

vectordb = Chroma.from_documents(documents=docs, embedding=embeddings, persist_directory=persist_directory)
vectordb.persist()
vectordb = None

# Load the persisted database from disk
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
retriever = vectordb.as_retriever(search_kwargs={"k": 2})

def generate_and_send_reports(config):
    """Generate reports and send them via email."""
    try:
        details_df = DataLoader.load_details(config.DETAILS_PATH)
    except Exception as e:
        logging.error(f"Failed to read details file: {e}")
        return

    insights_generator = InsightsGenerator(retriever)
    report_generator = ReportGenerator(config)
    email_sender = EmailSender(config)

    for index, row in details_df.iterrows():
        name, email = row['Name'], row['Email']
        file_path = os.path.join(config.BASE_DATA_PATH, f"{row['File name']}.xlsx")

        try:
            df = DataLoader.load_and_prepare_data(file_path, config.REPORT_TIMEFRAME)
            insights = insights_generator.generate_data_insights(df, retriever)
            filename_base = os.path.join(config.IMAGE_DIR, name)

            report_generator.plot_graphs(df, filename_base, config.REPORT_TIMEFRAME)
            tex_file_path = report_generator.generate_latex_report(name, insights, filename_base, config.REPORT_TIMEFRAME)
            pdf_path = report_generator.compile_latex_to_pdf(tex_file_path)

            if pdf_path:
                body_content = "Please find attached the Care Assessment Report."
                email_sender.send_email(pdf_path, email, f"{name}_Care_Assessment_{config.REPORT_TIMEFRAME}_Report.pdf", body_content)
            else:
                logging.error(f"Failed to compile LaTeX to PDF for {name}. Email not sent.")

        except Exception as e:
            logging.error(f"Failed to process data for {name}: {e}")

if __name__ == "__main__":
    generate_and_send_reports(Config)
