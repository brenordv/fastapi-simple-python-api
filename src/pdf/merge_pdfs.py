import PyPDF2
import io
from typing import List


def merge_pdfs(pdf_bytes_list: List[bytes]) -> bytes:
    """
    Merge multiple PDFs into a single PDF.

    :param pdf_bytes_list: List of byte objects, each representing a PDF file.
    :return: Byte content of the merged PDF file.
    """
    pdf_merger = PyPDF2.PdfMerger()

    for pdf_bytes in pdf_bytes_list:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        pdf_merger.append(pdf_reader)

    output = io.BytesIO()
    pdf_merger.write(output)
    output.seek(0)

    return output.getvalue()
