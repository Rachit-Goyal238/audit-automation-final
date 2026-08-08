import os

def create_output_paths(
    agency_code,
    agency_name,
    location,
    report_type,
    product,
    output_folder="output"
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    def sanitize(text):
        """Replaces invalid filename characters with an underscore."""
        return "".join(
            c if c.isalnum() or c in (" ", "_", "-", "(", ")") else "_" for c in text
        ).strip()

    s_agency_name = sanitize(agency_name)
    s_agency_code = sanitize(agency_code)
    s_location = sanitize(location)
    s_report_type = sanitize(report_type)
    s_product = sanitize(product)

    # Format: Agency Name (Agency Code) - Location - Report Type - Product
    base_name = f"{s_agency_name} ({s_agency_code}) - {s_location} - {s_report_type} - {s_product}"

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