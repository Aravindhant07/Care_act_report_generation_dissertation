import matplotlib.pyplot as plt
import seaborn as sns
from pylatex import Document, Figure, Package, Command, NoEscape, Section
import os
import subprocess
import logging

class ReportGenerator:
    def __init__(self, config):
        self.config = config

    def plot_graphs(self, df, filename_base):
        color_palette = ['#9d1d7f', '#283162', '#00ffff', '#e4245e']

        for column in df.columns.difference(['Timestamp']):
            plt.figure(figsize=(12, 6))
            sns.lineplot(x='Timestamp', y=column, data=df, marker='o', color=color_palette[0])
            plt.title(f'{column} Trend Over Time')
            plt.xlabel('Time')
            plt.ylabel(f'{column}')
            plt.grid(True)
            plt.savefig(f'{filename_base}_{column}_line.png')
            plt.close()

        plt.figure(figsize=(12, 6))
        for column in df.columns.difference(['Timestamp']):
            sns.lineplot(x='Timestamp', y=column, data=df, marker='o')
        plt.title('Overall Trend of All Columns Over Time')
        plt.xlabel('Time')
        plt.ylabel('Scores')
        plt.legend(df.columns.difference(['Timestamp']), loc='upper left')
        plt.grid(True)
        plt.savefig(f'{filename_base}_overall_trend.png')
        plt.close()

    def generate_latex_report(self, name, insights, filename_base):
        doc = Document(document_options='10pt, a4paper', documentclass='article')
        self._setup_document_style(doc)

        doc.preamble.append(Command('title', f'{name} Care Assessment Report'))
        doc.preamble.append(Command('author', 'Automated Analysis System'))
        doc.preamble.append(Command('date', NoEscape(r'\today')))
        doc.append(NoEscape(r'\maketitle'))

        with doc.create(Section('Introduction and Basic Information')):
            doc.append(f"This report provides an assessment of {name}'s current care needs based on recent data.")
            overall_trend_path = f"{filename_base}_overall_trend.png"
            if os.path.exists(overall_trend_path):
                with doc.create(Figure(position='H')) as fig:
                    fig.add_image(overall_trend_path, width=NoEscape(r'0.8\textwidth'))
                    fig.add_caption('Overall Trend of All Columns')

        for column, insight_text in insights.items():
            renamed_column = column.replace('Clothed', 'Being appropriately clothed').replace('Out of home', 'Out of home score')
            with doc.create(Section(f'Insight on {renamed_column}')):
                doc.append(insight_text)
                self._include_graph(doc, filename_base, column)

        doc.append(NoEscape(r'\end{document}'))
        tex_filename = f"{self.config['report_dir']}/{name}_Care_Assessment_Report.tex"
        doc.generate_tex(tex_filename)
        return tex_filename

    def _setup_document_style(self, doc):
        doc.preamble.append(Package('geometry', options='top=3cm, bottom=3cm, left=2.5cm, right=2.5cm'))
        doc.preamble.append(Package('graphicx'))

    def _include_graph(self, doc, filename_base, column):
        graph_filename = f"{filename_base}_{column}_line.png"
        if os.path.exists(graph_filename):
            with doc.create(Figure(position='H')) as fig:
                fig.add_image(graph_filename, width=NoEscape(r'0.8\textwidth'))
                fig.add_caption(f'Line graph of {column} over time')

    def compile_latex_to_pdf(self, tex_file_path):
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
