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

    header = PageStyle("header")
    with header.create(Head("L")):
        header_image_path = normalize_path(config['HEADER_IMAGE'])
        with MiniPage(width=r"0.49\textwidth", pos='c'):
            header.append(StandAloneGraphic(header_image_path, width=r"0.9\textwidth"))
    with header.create(Head("R")):
        with MiniPage(width=r"0.49\textwidth", pos='c'):
            header.append(r"\today")

    footer = PageStyle("footer")
    with footer.create(Foot("C")):
        footer_image_path = normalize_path(config['FOOTER_IMAGE'])
        with MiniPage(width=r"0.6\textwidth", pos='c'):
            footer.append(StandAloneGraphic(footer_image_path, width=r"0.9\textwidth"))

    doc.preamble.append(header)
    doc.preamble.append(footer)
    doc.change_document_style("header")

    doc.preamble.append(Command('setlength', '\\headheight', '60pt'))
    doc.preamble.append(Command('setlength', '\\footskip', '40pt'))
    doc.preamble.append(Command('setlength', '\\headsep', '20pt'))
    doc.preamble.append(Command('setlength', '\\textheight', '680pt'))

    doc.preamble.append(NoEscape(r'\fancypagestyle{plain}{\fancyhf{}\fancyhead[L]{\includegraphics[width=4cm]{%s}}\fancyfoot[C]{\includegraphics[width=4cm]{%s}}}' % (header_image_path, footer_image_path)))
    doc.preamble.append(Command('pagestyle', 'plain'))

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
