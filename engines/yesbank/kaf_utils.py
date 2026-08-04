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

    insert_at = template_end_row

    for _ in range(
        rows_needed
    ):

        ws.insert_rows(
            insert_at
        )

        copy_row_style(
            ws,
            template_style_row,
            insert_at
        )

        insert_at += 1


def populate_kaf(
    ws,
    kaf_file,
    agency_name,
    source_sheet
):

    df = pd.read_excel(
        kaf_file,
        sheet_name=source_sheet,
        keep_default_na=False
    )

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )

    if "Vendor Name" not in df.columns:

        raise Exception(
            f"'Vendor Name' column not found in {source_sheet} sheet."
        )

    df = df[
        df["Vendor Name"]
        .astype(str)
        .str.strip()
        ==
        agency_name.strip()
    ]

    start_row = 2

    if source_sheet == "Collection":

        template_style_row = 15
        template_end_row = 16
        template_capacity = 15

        ensure_capacity(
            ws,
            len(df),
            template_style_row,
            template_end_row,
            template_capacity
        )

    elif source_sheet == "Repo":

        template_style_row = 7
        template_end_row = 8
        template_capacity = 6

        ensure_capacity(
            ws,
            len(df),
            template_style_row,
            template_end_row,
            template_capacity
        )

    elif source_sheet == "Final Stock":

        template_style_row = 7
        template_end_row = 8
        template_capacity = 6

        ensure_capacity(
            ws,
            len(df),
            template_style_row,
            template_end_row,
            template_capacity
        )

    else:

        raise Exception(
            f"Unsupported KAF sheet: {source_sheet}"
        )

    for idx, row in enumerate(
        df.itertuples(index=False)
    ):

        excel_row = (
            start_row
            + idx
        )

        for col_idx in range(
            1,
            30
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