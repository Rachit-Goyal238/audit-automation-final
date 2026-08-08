import os
import re

def create_output_paths(
    agency_name,
    agency_code,
    location,
    report_type,
    product,
    output_folder="output"
):
    os.makedirs(
        output_folder,
        exist_ok=True
    )

    # Format: Agency Name (Agency Code) - Location - Report Type - Product
    base_name_raw = (
        f"{agency_name} ({agency_code}) - {location} - {report_type} - {product}"
    )

    # Sanitize the filename to remove characters illegal in Windows/Linux file paths
    base_name = re.sub(r'[\\/*?:"<>|]', "", base_name_raw)
    # Replace any lingering double spaces with a single space for cleanliness
    base_name = re.sub(r'\s+', ' ', base_name).strip()

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