import subprocess
import os
import platform


def compress_pdf(input_bytes, quality='ebook'):
    """
    Compress a PDF file using GhostScript.

    :param input_bytes: Byte content of the input PDF file.
    :param quality: Compression level. Options are:
        - 'screen': lower quality, smaller size (72 dpi)
        - 'ebook': for better quality, but slightly larger pdfs (150 dpi)
        - 'printer': high quality, larger pdfs (300 dpi)
        - 'prepress': high quality, color preserving, largest pdfs (300 dpi)
    :return: Byte content of the compressed PDF file.
    """

    # Validate the quality parameter
    valid_qualities = ['screen', 'ebook', 'printer', 'prepress']
    if quality not in valid_qualities:
        raise ValueError(f"Invalid quality setting. Choose from: {', '.join(valid_qualities)}")

    # Determine the GhostScript command based on the operating system
    gs_command = 'gswin64c' if platform.system() == 'Windows' else 'gs'

    input_path = 'temp_input.pdf'
    output_path = 'temp_output.pdf'

    with open(input_path, 'wb') as f:
        f.write(input_bytes)

    subprocess.run([
        gs_command, '-sDEVICE=pdfwrite', '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS=/{quality}', '-dNOPAUSE', '-dQUIET', '-dBATCH',
        f'-sOutputFile={output_path}', input_path
    ], check=True)

    with open(output_path, 'rb') as f:
        output_bytes = f.read()

    # Clean up temporary files
    os.remove(input_path)
    os.remove(output_path)

    yield output_bytes
