import os
import re
import fitz
import pandas as pd
import json
import subprocess

from pypdf import PdfReader, PdfWriter


def extract_pdf_header(pdf_path):

    pdf = fitz.open(pdf_path)

    page = pdf[0]

    text = page.get_text()

    lines = [
        line.strip()
        for line in text.split("\n")
        if line.strip()
    ]

    data = {}

    for i, line in enumerate(lines):

        try:

            if line == "AGENCY NAME":
                data["agency_name"] = lines[i + 1]

            elif line == "OPERATING ADDRESS":

                address_lines = []

                j = i + 1

                while j < len(lines):

                    if lines[j] == "CURRENT EMAIL ID":
                        break

                    address_lines.append(lines[j])

                    j += 1

                data["operating_address"] = " ".join(
                    address_lines
                )

            elif line == "TYPE OF AGENCY":
                data["agency_type"] = lines[i + 1]

            elif line == "COLLECTION MANAGER":
                data["collection_manager"] = lines[i + 1]

            elif line == "AGENCY MANAGER":
                data["agency_manager"] = lines[i + 1]

        except IndexError:
            pass

    pdf.close()

    return data

def extract_evidence_pages(input_pdf, output_pdf):

    pdf = fitz.open(input_pdf)

    evidence_pdf = fitz.open()

    for page_num in range(len(pdf)):

        page = pdf[page_num]

        text = page.get_text()

        if re.search(
            r"Observation\s*#?\s*\d+",
            text,
            re.IGNORECASE
        ):

            evidence_pdf.insert_pdf(
                pdf,
                from_page=page_num,
                to_page=page_num
            )

    evidence_pdf.save(output_pdf)

    evidence_pdf.close()
    pdf.close()

def merge_pdfs(pdf1, pdf2, pdf3, output_pdf):

    writer = PdfWriter()

    for pdf_file in [pdf1, pdf2, pdf3]:

        if not pdf_file:
            continue
        
        reader = PdfReader(pdf_file)

        for page in reader.pages:
            writer.add_page(page)

    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

import shutil
import subprocess
import os


def excel_to_pdf(
    excel_path,
    pdf_path
):

    soffice_path = shutil.which(
        "soffice"
    )

    if not soffice_path:

        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
        ]

        for path in possible_paths:

            if os.path.exists(path):

                soffice_path = path

                break

    if not soffice_path:

        raise Exception(
            "LibreOffice not installed"
        )

    output_dir = os.path.dirname(
        os.path.abspath(pdf_path)
    )

    subprocess.run(
        [
            soffice_path,
            "--headless",
            "--convert-to",
            "pdf",
            os.path.abspath(excel_path),
            "--outdir",
            output_dir
        ],
        check=True
    )

    generated_pdf = os.path.join(
        output_dir,
        os.path.splitext(
            os.path.basename(excel_path)
        )[0] + ".pdf"
    )

    if os.path.abspath(
        generated_pdf
    ) != os.path.abspath(
        pdf_path
    ):

        os.replace(
            generated_pdf,
            pdf_path
        )