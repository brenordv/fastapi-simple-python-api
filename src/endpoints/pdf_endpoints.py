from enum import Enum
import io
from typing import List
from zipfile import ZipFile

from fastapi import File, UploadFile, APIRouter, Response, Query, HTTPException
from fastapi.responses import StreamingResponse

from pdf.compress_pdf import compress_pdf
from pdf.merge_pdfs import merge_pdfs
from pdf.split_pdf import split_pdf


class CompressionQuality(str, Enum):
    screen = 'screen'
    ebook = 'ebook'
    printer = 'printer'
    prepress = 'prepress'


def configure_pdf_endpoints(prefix):
    pdf_endpoints = APIRouter(prefix=f"{prefix}/pdf", tags=["PDF"])
    @pdf_endpoints.post("/compress", status_code=200,
                        summary="Compresses a PDF file.")
    async def compress_pdf_endpoint(
            uploaded_file: UploadFile = File(..., description="The PDF file to be compressed."),
            quality: CompressionQuality = CompressionQuality.ebook):
        """
        Compresses a PDF file.
        This endpoint accepts a PDF file and a compression quality level. It returns the compressed PDF.

        Remarks:
        - Quality of 'screen' may generate an unreadable PDF.\n
        - This endpoint relies on Ghostscript. Since the API is up, this shouldn't matter... just saying, so you know.

        """

        # Check if the uploaded file is a PDF by its MIME type
        if uploaded_file.content_type != 'application/pdf':
            return {"error": "The uploaded file is not a PDF."}

        # Read the uploaded PDF file
        input_pdf_bytes = await uploaded_file.read()
        output_pdf_bytes = compress_pdf(input_pdf_bytes, quality)

        # Create a StreamingResponse to return the compressed PDF
        return StreamingResponse(
            output_pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=compressed_{uploaded_file.filename}"
            }
        )


    @pdf_endpoints.post("/split", status_code=200,
                        summary="Splits a PDF file into two parts.")
    async def split_pdf_endpoint(
            file: UploadFile = File(..., description="The PDF file to be split."),
            split_page: int = Query(description="Page number to split the PDF")):
        """
        Splits a PDF file into two parts.

        This endpoint accepts a PDF file and a page number to split the PDF at. It returns a ZIP file
        containing the two parts.
        """
        input_bytes = await file.read()
        part1_bytes, part2_bytes = split_pdf(input_bytes, split_page)

        # Create a ZIP file in memory
        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, 'w') as zip_file:
            # Save each part as a file in the ZIP
            zip_file.writestr('part1.pdf', part1_bytes)
            zip_file.writestr('part2.pdf', part2_bytes)

        # Prepare the ZIP file to be sent as a response
        zip_buffer.seek(0)
        return Response(content=zip_buffer.read(),
                        media_type="application/zip",
                        headers={"Content-Disposition": "attachment; filename=split_pdf.zip"})


    @pdf_endpoints.post("/merge", status_code=200,
                        summary="Merges multiple PDF files into a single PDF.")
    async def merge_pdfs_endpoint(files: List[UploadFile] = File(..., description="The PDF files to be merged.")):
        """
        Receives multiple PDF files and merges them into a single PDF.
        Returns the bytes of the merged PDF.
        """
        if not files:
            raise HTTPException(status_code=400, detail="No files were uploaded.")

        pdf_bytes_list = []
        for file in files:
            content = await file.read()
            pdf_bytes_list.append(content)
            await file.close()  # Close the file explicitly

        merged_pdf_bytes = merge_pdfs(pdf_bytes_list)

        return Response(content=merged_pdf_bytes,
                        media_type="application/pdf",
                        headers={"Content-Disposition": "attachment; filename=merged.pdf"})

    return pdf_endpoints
