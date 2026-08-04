import os

def create_output_paths(
    agency_code,
    agency_name,
    output_folder="output"
):

    os.makedirs(
        output_folder,
        exist_ok=True
    )

    safe_agency_name = "".join(
        c if c.isalnum() or c in (" ", "_", "-")
        else "_"
        for c in agency_name
    ).replace(
        " ",
        "_"
    )

    base_name = (
        f"{agency_code}_{safe_agency_name}"
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