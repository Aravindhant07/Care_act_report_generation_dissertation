from pylatex import Document, PageStyle, Head, Foot, MiniPage, StandAloneGraphic, Command
from pylatex.utils import NoEscape
import os
import logging

def normalize_path(path):
    """Normalize file path for LaTeX compatibility."""
    return path.replace('\\', '/')

def setup_document_style(doc, config):
    """Setup the document style for LaTeX report."""
    doc.preamble.append(Package('geometry', options='top=3cm, bottom=3cm, left=2.5cm, right=2.5cm'))
    doc.preamble.append(Package('graphicx'))

   

def include_graphs(doc, filename_base, column, timeframe):
    """Include graphs into the LaTeX document based on available types."""
    graph_filename = f"{filename_base}_{column}_{timeframe}_line.png"
    full_path = os.path.join(CONFIG['IMAGE_DIR'], graph_filename)
    if os.path.exists(full_path):
        doc.append(NoEscape(r'\begin{figure}[H]'))
        doc.append(NoEscape(r'\centering'))
        doc.append(NoEscape(r'\includegraphics[width=0.8\textwidth]{%s}' % normalize_path(full_path)))
        doc.append(NoEscape(r'\caption{%s of %s over time}' % ("line", column)))
        doc.append(NoEscape(r'\end{figure}'))
    else:
        logging.info(f"Graph type Line for column '{column}' not found.")
