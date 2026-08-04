import pandas as pd

from engines.yesbank.yesbank_main import (
    generate_yesbank_report
)


print(
    "\nSelect Report Type:"
)

print(
    "1. Collection"
)

print(
    "2. Repo"
)

print(
    "3. Stockyard"
)


choice = input(
    "\nEnter Choice (1-3): "
).strip()


report_types = {

    "1": "Collection",

    "2": "Repo",

    "3": "Stockyard"

}


if choice not in report_types:

    raise Exception(
        "Invalid Choice."
    )


REPORT_TYPE = report_types[
    choice
]


BASE_DATA_FILE = "Base_Data.xlsx"

KAF_FILE = "KAF.xlsx"

ANNEXURE_FILE = "Annexure.xlsx"

VEHICLE_DETAILS_FILE = "Vehicle Details.xlsx"


if REPORT_TYPE == "Collection":

    TEMPLATE_FILE = (
        "templates/YesBank/YesBank_Collection_Template_2026-27.xlsx"
    )

elif REPORT_TYPE == "Repo":

    TEMPLATE_FILE = (
        "templates/YesBank/YesBank_Repossesion_Template_2026-27.xlsx"
    )

else:

    TEMPLATE_FILE = (
        "templates/YesBank/YesBank_Stockyard_Template_2026-27.xlsx"
    )


print(
    "\nBase Data Sheets:"
)

print(
    pd.ExcelFile(
        BASE_DATA_FILE
    ).sheet_names
)


print(
    "\nKAF Sheets:"
)

print(
    pd.ExcelFile(
        KAF_FILE
    ).sheet_names
)


if REPORT_TYPE == "Collection":

    print(
        "\nAnnexure Sheets:"
    )

    print(
        pd.ExcelFile(
            ANNEXURE_FILE
        ).sheet_names
    )


if REPORT_TYPE == "Stockyard":

    print(
        "\nVehicle Details Sheets:"
    )

    print(
        pd.ExcelFile(
            VEHICLE_DETAILS_FILE
        ).sheet_names
    )


agency_name = input(
    "\nEnter Agency Name: "
).strip()


output_file = generate_yesbank_report(

    report_type=REPORT_TYPE,

    base_data_file=BASE_DATA_FILE,

    kaf_file=KAF_FILE,

    annexure_file=(
        ANNEXURE_FILE
        if REPORT_TYPE == "Collection"
        else None
    ),

    vehicle_details_file=(
        VEHICLE_DETAILS_FILE
        if REPORT_TYPE == "Stockyard"
        else None
    ),

    template_file=TEMPLATE_FILE,

    agency_name=agency_name

)


print(
    "\n===================================="
)

print(
    f"YESBANK {REPORT_TYPE.upper()} TEST COMPLETED"
)

print(
    f"Agency : {agency_name}"
)

print(
    f"Output : {output_file}"
)

print(
    "===================================="
)