import matplotlib.pyplot as plt
import seaborn as sns
from pylatex import Document, Section, Command, Package, Figure
from utils.latex_helper import setup_document_style, include_graphs, normalize_path
import os
import logging
import subprocess

class ReportGenerator:
    def __init__(self, config):
        self.config = config

    def plot_graphs(self, df, filename_base, timeframe):
        """Plot graphs for each column and save as images."""
        color_palette = ['#9d1d7f', '#283162', '#00ffff', '#e4245e']

        for column in df.columns.difference(['Timestamp']):
            plt.figure(figsize=(12, 6))
            sns.lineplot(x='Timestamp', y=column, data=df, marker='o', color=color_palette[0])
            plt.title(f'{column} Trend Over Time')
            plt.xlabel('Time')
            plt.ylabel(f'{column}')
            plt.grid(True)
            plt.savefig(f'{filename_base}_{column}_{timeframe}_line.png')
            plt.close()

        plt.figure(figsize=(12, 6))
        for column in df.columns.difference(['Timestamp']):
            sns.lineplot(x='Timestamp', y=column, data=df, marker='o')
        plt.title('Overall Trend of All Columns Over Time')
        plt.xlabel('Time')
        plt.ylabel('Scores')
        plt.legend(df.columns.difference(['Timestamp']), loc='upper left')
        plt.grid(True)
        plt.savefig(f'{filename_base}_overall_trend_{timeframe}.png')
        plt.close()

    def generate_latex_report(self, name, insights, filename_base, timeframe):
        """Generate LaTeX report with dynamic content and graphs."""
        doc = Document(document_options='10pt, a4paper', documentclass='article')
        setup_document_style(doc, self.config)

        doc.preamble.append(Command('title', f'{name} Care Assessment Report'))
        doc.preamble.append(Command('author', 'Automated Analysis System'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))

        with doc.create(Section('Introduction and Basic Information')):
            doc.append(f"This report provides an assessment of {name}'s current care needs based on recent data.")
            overall_trend_path = os.path.join(self.config['IMAGE_DIR'], f"{filename_base}_overall_trend_{timeframe}.png")
            if os.path.exists(overall_trend_path):
                doc.append(NoEscape(r'\begin{figure}[H]'))
                doc.append(NoEscape(r'\centering'))
                doc.append(NoEscape(r'\includegraphics[width=0.8\textwidth]{%s}' % normalize_path(overall_trend_path)))
                doc.append(NoEscape(r'\caption{Overall Trend of All Columns}'))
                doc.append(NoEscape(r'\end{figure}'))

            if 'Frailty score' in insights:
                with doc.create(Section('Executive Summary: Insight on Frailty score')):
                    doc.append(insights['Frailty score'])
                    include_graphs(doc, filename_base, 'Frailty score', timeframe)

        for column, insight_text in insights.items():
            if column != 'Frailty score':
                renamed_column = column.replace('Clothed', 'Being appropriately clothed').replace('Out of home', 'Out of home score')
                with doc.create(Section(f'Insight on {renamed_column}')):
                    doc.append(insight_text)
                    include_graphs(doc, filename_base, column, timeframe)

        doc.append(NoEscape(r'\end{document}'))
        tex_filename = os.path.join(self.config['REPORT_DIR'], f"{name}_Care_Assessment_Report.tex")
        doc.generate_tex(normalize_path(tex_filename))
        return normalize_path(tex_filename)

    def compile_latex_to_pdf(self, tex_file_path):
        """Compile LaTeX document to PDF."""
        directory, tex_file = os.path.split(tex_file_path + '.tex')
        command = ["xelatex", "-interaction=nonstopmode", tex_file]
        try:
            result = subprocess.run(command, cwd=directory, capture_output=True, text=True)
            if result.returncode != 0:
                logging.error(f"LaTeX compilation failed: {result.stderr}")
                return None
            return tex_file_path.replace('.tex', '.pdf')
        except subprocess.CalledProcessError as e:
            logging.error(f"LaTeX compilation process failed: {e.stderr}")
            return None
