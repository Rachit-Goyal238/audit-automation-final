from openpyxl import load_workbook

from engines.yesbank.schedule_utils import (
    get_schedule_info,
    get_output_filename
)

from engines.yesbank.rating_utils import (
    populate_rating
)

from engines.yesbank.kaf_utils import (
    populate_kaf
)

from engines.yesbank.stockyard_kaf_utils import (
    populate_stockyard_kaf
)

from engines.yesbank.agency_utils import (
    populate_agency
)

from engines.yesbank.annexure_utils import (
    populate_annexure_1,
    populate_annexure_2
)

from engines.yesbank.vehicle_details_utils import (
    populate_vehicle_details
)


def generate_yesbank_report(
    report_type,
    base_data_file,
    kaf_file,
    annexure_file,
    vehicle_details_file,
    template_file,
    agency_name
):

    schedule_info = get_schedule_info(
        base_data_file,
        agency_name
    )

    audit_period = schedule_info[
        "audit_period"
    ]

    output_file = get_output_filename(
        schedule_info,
        report_type
    )

    wb = load_workbook(
        template_file
    )

    print(
        "Populating Rating..."
    )

    populate_rating(
        wb["Rating"],
        base_data_file,
        agency_name,
        audit_period
    )

    print(
        "Populating KAF..."
    )

    if report_type == "Stockyard":

        populate_stockyard_kaf(
            wb["KAF"],
            kaf_file,
            agency_name
        )

    else:

        populate_kaf(
            wb["KAF"],
            kaf_file,
            agency_name,
            report_type
        )

    if report_type == "Stockyard":

        print(
            "Populating Checklist..."
        )

        populate_agency(
            agency_ws=wb["Checklist"],
            kaf_ws=wb["KAF"],
            kaf_observation_col=11,
            status_col=9,
            errors_col=10,
            agency_observation_col=12
        )

        print(
            "Populating Vehicle Details..."
        )

        populate_vehicle_details(
            wb["Vehicle Details"],
            vehicle_details_file,
            agency_name
        )

    else:

        print(
            "Populating Agency..."
        )

        populate_agency(
            agency_ws=wb["Agency"],
            kaf_ws=wb["KAF"],
            kaf_observation_col=9,
            status_col=8,
            errors_col=9,
            agency_observation_col=12
        )

    if report_type == "Collection":

        print(
            "Populating Annexure 1..."
        )

        populate_annexure_1(
            wb["Annexure 1"],
            annexure_file,
            agency_name
        )

        print(
            "Populating Annexure 2..."
        )

        populate_annexure_2(
            wb["Annexure 2"],
            annexure_file,
            agency_name
        )

    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True

    wb.save(
        output_file
    )

    print()

    print(
        f"{report_type} report generated successfully."
    )

    print(
        f"Saved as: {output_file}"
    )

    return output_file