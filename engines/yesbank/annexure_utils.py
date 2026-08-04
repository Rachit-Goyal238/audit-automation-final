from copy import copy
import pandas as pd


def copy_row_style(
    ws,
    source_row,
    target_row
):

    for col in range(
        1,
        ws.max_column + 1
    ):

        source = ws.cell(
            source_row,
            col
        )

        target = ws.cell(
            target_row,
            col
        )

        target._style = copy(
            source._style
        )

    ws.row_dimensions[
        target_row
    ].height = ws.row_dimensions[
        source_row
    ].height



def ensure_capacity(
    ws,
    required_rows,
    template_style_row,
    template_end_row,
    template_capacity
):

    if required_rows <= template_capacity:

        return

    rows_needed = (
        required_rows
        - template_capacity
    )

    source_styles = {}

    for col in range(
        1,
        ws.max_column + 1
    ):

        source_styles[col] = copy(
            ws.cell(
                template_style_row,
                col
            )._style
        )

    insert_at = template_end_row

    for _ in range(
        rows_needed
    ):

        ws.insert_rows(
            insert_at
        )

        for col in range(
            1,
            ws.max_column + 1
        ):

            ws.cell(
                insert_at,
                col
            )._style = copy(
                source_styles[col]
            )

        insert_at += 1



def resize_column(
    ws,
    column_letter,
    start_row,
    end_row
):

    max_length = 0

    for row in range(
        start_row,
        end_row + 1
    ):

        value = ws[
            f"{column_letter}{row}"
        ].value

        if value:

            max_length = max(
                max_length,
                len(str(value))
            )

    ws.column_dimensions[
        column_letter
    ].width = max_length + 10


def populate_annexure_1(
    ws,
    annexure_file,
    agency_name
):
    print(f"Populating Annexure 1 for: {agency_name}")
    df = pd.read_excel(
        annexure_file,
        sheet_name="Annexure 1",
        keep_default_na=False
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    if "Agency Name" not in df.columns:

        raise Exception(
            "'Agency Name' column not found in Annexure 1"
        )

    df = df[
        df["Agency Name"]
        .astype(str)
        .str.strip()
        ==
        agency_name.strip()
    ]
    print(f"Annexure 1 rows found: {len(df)}")
    start_row = 4

    template_style_row = 7
    template_end_row = 8
    template_capacity = 5

    ensure_capacity(
        ws,
        len(df),
        template_style_row,
        template_end_row,
        template_capacity
    )

    for idx, row in enumerate(
        df.itertuples(index=False)
    ):

        excel_row = (
            start_row + idx
        )

        for col_idx in range(
            1,
            9
        ):

            value = row[
                col_idx - 1
            ]

            if pd.isna(
                value
            ):

                value = ""

            ws.cell(
                excel_row,
                col_idx
            ).value = value

    if len(df) > 0:

        final_data_row = (
            start_row
            + len(df)
            - 1
        )

        resize_column(
            ws,
            "H",
            start_row,
            final_data_row
        )
        print("Annexure 1 done")


def populate_annexure_2(
    ws,
    annexure_file,
    agency_name
):
    print(f"Populating Annexure 2 for: {agency_name}")
    df = pd.read_excel(
        annexure_file,
        sheet_name="Annexure 2",
        keep_default_na=False
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    if "Agency Name" not in df.columns:

        raise Exception(
            "'Agency Name' column not found in Annexure 2"
        )

    df = df[
        df["Agency Name"]
        .astype(str)
        .str.strip()
        ==
        agency_name.strip()
    ]
    print(f"Annexure 2 rows found: {len(df)}")
    start_row = 4

    template_style_row = 19
    template_end_row = 20
    template_capacity = 17

    ensure_capacity(
        ws,
        len(df),
        template_style_row,
        template_end_row,
        template_capacity
    )

    for idx, row in enumerate(
        df.itertuples(index=False)
    ):

        excel_row = (
            start_row + idx
        )

        for col_idx in range(
            1,
            7
        ):

            value = row[
                col_idx - 1
            ]

            if pd.isna(
                value
            ):

                value = ""

            ws.cell(
                excel_row,
                col_idx
            ).value = value

    if len(df) > 0:

        final_data_row = (
            start_row
            + len(df)
            - 1
        )

        resize_column(
            ws,
            "F",
            start_row,
            final_data_row
        )
        print("Annexure 2 done")