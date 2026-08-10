"""
Extracts all observations where Compliance Status = No.
"""

from typing import List

from email_module.models.observation import Observation


class ObservationsExtractor:

    def __init__(self, worksheet, config):
        self.ws = worksheet
        self.config = config

    def extract(self) -> List[Observation]:

        header_row = self._find_header_row()

        column_map = self._build_column_map(header_row)

        cols = self.config["checklist"]["columns"]

        filter_column = self.config["checklist"]["filter"]["column"]

        filter_value = self.config["checklist"]["filter"]["value"]

        observations = []

        row = header_row + 1

        while True:

            sr_no = self.ws.cell(
                row=row,
                column=self._require_column(
                    column_map,
                    cols["sr_no"]
                )
            ).value

            if sr_no in (None, ""):
                break

            status = self._cell(
                row,
                self._require_column(
                    column_map,
                    filter_column
                )
            )

            if status.lower() == filter_value.lower():

                observations.append(

                    Observation(

                        rating_category=self._cell(
                            row,
                            self._require_column(
                                column_map,
                                cols["rating_category"]
                            )
                        ),

                        short_segmentation=self._cell(
                            row,
                            self._require_column(
                                column_map,
                                cols["short_segmentation"]
                            )
                        ),

                        observation=self._cell(
                            row,
                            self._require_column(
                                column_map,
                                cols["observation"]
                            )
                        ),

                        pending_status=self._cell(
                            row,
                            self._require_column(
                                column_map,
                                cols["pending_status"]
                            )
                        )

                    )

                )

            row += 1

        return observations

    def _find_header_row(self):

        search_text = self.config["checklist"]["table_start_search"]

        for row in self.ws.iter_rows():

            for cell in row:

                if cell.value is None:
                    continue

                if self._normalize_header(cell.value) == search_text:
                    return cell.row

        raise Exception("Checklist header row not found.")

    def _normalize_header(self, header):

        header = str(header)

        header = header.replace("\n", " ")

        header = " ".join(header.split())

        return header.strip()

    def _build_column_map(self, header_row):

        columns = {}

        for cell in self.ws[header_row]:

            if cell.value is None:
                continue

            columns[
                self._normalize_header(cell.value)
            ] = cell.column

        return columns

    def _cell(self, row, column):

        value = self.ws.cell(
            row=row,
            column=column
        ).value

        if value is None:
            return ""

        return str(value).strip()

    def _require_column(self, column_map, column_name):

        if column_name not in column_map:

            available = "\n".join(column_map.keys())

            raise Exception(
                f"Required column '{column_name}' not found.\n\n"
                f"Available columns:\n{available}"
            )

        return column_map[column_name]