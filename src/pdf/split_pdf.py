import PyPDF2
import io
from typing import Tuple


def split_pdf(pdf_bytes: bytes, split_page: int) -> Tuple[bytes, bytes]:
    """
    Split a PDF file at a specific page number into two separate files.

    :param pdf_bytes: Byte content of the input PDF file.
    :param split_page: The page number at which to split the PDF.
    :return: A tuple containing byte contents of the two split PDF files.
    """
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))

    num_pages = len(reader.pages)
    if split_page < 1 or split_page >= num_pages:
        raise ValueError("Split page must be between 1 and the number of pages in the PDF.")

    writer1 = PyPDF2.PdfWriter()
    writer2 = PyPDF2.PdfWriter()

    for i in range(num_pages):
        if i <= split_page:
            writer1.add_page(reader.pages[i])
        else:
            writer2.add_page(reader.pages[i])

    output1 = io.BytesIO()
    writer1.write(output1)
    output1.seek(0)

    output2 = io.BytesIO()
    writer2.write(output2)
    output2.seek(0)

    return output1.getvalue(), output2.getvalue()
