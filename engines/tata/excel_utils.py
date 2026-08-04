from copy import copy
import re


def parse_closing_comment(comment):

    parts = [
        p.strip()
        for p in re.split(r"\s*[|;]\s*", str(comment))
    ]

    return {

        "remarks":
            parts[0] if len(parts) > 0 else "",

        "status":
            parts[1] if len(parts) > 1 else "",

        "timeline":
            parts[2] if len(parts) > 2 else ""
    }


def populate_headers(
    ws,
    first_row,
    pdf_data
):

    ws["D2"] = first_row["Agency Code"]
    ws["D3"] = first_row["Agency Name"]

    ws["D4"] = pdf_data.get(
        "operating_address",
        ""
    )

    ws["D5"] = pdf_data.get(
        "agency_type",
        ""
    )

    ws["G2"] = first_row["Auditor Name"]

    audit_date_col = next(
        (
            col for col in first_row.keys()
            if "audit" in str(col).lower() and "date" in str(col).lower()
        ),
        None
    )

    if audit_date_col:
        ws["G3"] = first_row[audit_date_col]
    else:
        ws["G3"] = "Date Not Found"

    ws["G4"] = pdf_data.get(
        "collection_manager",
        ""
    )

    ws["G5"] = pdf_data.get(
        "agency_manager",
        ""
    )


def populate_checklist(
    ws,
    audit_df
):

    question_row_map = {}

    for r in range(
        8,
        ws.max_row + 1
    ):

        try:

            sr_no = int(
                ws[f"A{r}"].value
            )

            question_row_map[
                sr_no
            ] = r

        except:
            pass

    print(
        f"Template Questions Found: {len(question_row_map)}"
    )

    populated_count = 0

    for _, audit_row in audit_df.iterrows():

        try:

            question_no = int(
                str(
                    audit_row["Question No."]
                ).strip()
            )

        except:
            continue

        if question_no not in question_row_map:

            print(
                f"Question {question_no} not found in template"
            )

            continue

        excel_row = question_row_map[
            question_no
        ]

        status = str(
            audit_row["Status Detail"]
        ).strip()

        ws[f"F{excel_row}"] = status

        ws[f"G{excel_row}"] = str(
            audit_row["Key Observation"]
        ).strip()

        parsed = parse_closing_comment(
            audit_row["Remarks"]
        )

        ws[f"H{excel_row}"] = parsed["remarks"]

        ws[f"I{excel_row}"] = parsed["status"]

        ws[f"J{excel_row}"] = parsed["timeline"]

        if status.upper() in [
            "NO",
            "NA"
        ]:

            for col in [
                "F",
                "G",
                "H",
                "I",
                "J"
            ]:

                cell = ws[
                    f"{col}{excel_row}"
                ]

                font = copy(
                    cell.font
                )

                font.bold = True

                cell.font = font

        populated_count += 1

    print(
        f"Questions Populated: {populated_count}"
    )