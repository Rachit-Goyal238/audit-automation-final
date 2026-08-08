import os
import re

def create_output_paths(
    agency_code,
    agency_name,
    location,
    report_type,
    product,
    output_folder="output"
):
    """
    Generates a dictionary of output file paths for a given agency.

    This function sanitizes the agency name to create a safe base filename
    and constructs full paths for various report files (Excel, PDF, etc.).

    Args:
        agency_code (str): The agency's unique code.
        agency_name (str): The agency's name.
        location (str): The agency's location.
        report_type (str): The type of report/agency.
        product (str): The product associated with the report.
        output_folder (str, optional): The directory to store output files.
                                      Defaults to "output".

    Returns:
        dict: A dictionary mapping file types to their full paths.
    """

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    def sanitize(text):
        # Replace invalid filename characters with an underscore
        return re.sub(r'[<>:"/\\|?*]', '_', str(text)).strip()

    s_agency_name = sanitize(agency_name)
    s_agency_code = sanitize(agency_code)
    s_location = sanitize(location)
    s_report_type = sanitize(report_type)
    s_product = sanitize(product)

    base_name = (
        f"{s_agency_name} ({s_agency_code}) - {s_location} - "
        f"{s_report_type} - {s_product}"
    )

    return {

        "excel": os.path.join(
            output_folder,
            f"{base_name}.xlsx"
        ),

        "pdf": os.path.join(
            output_folder,
            f"{base_name}.pdf"
        ),

        "evidence": os.path.join(
            output_folder,
            f"{base_name}_Evidence.pdf"
        ),

        "final": os.path.join(
            output_folder,
            f"{base_name}_Final_Report.pdf"
        )
    }