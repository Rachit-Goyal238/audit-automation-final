"""
Extracts the Score Parameters table.
"""
class ScoreTableExtractor:

    def __init__(self, worksheet):
        self.ws = worksheet

    def extract(self):

        scores = []

        # Row 1 contains the headers
        header_row = 1

        headers = {}

        for cell in self.ws[header_row]:

            if cell.value is None:
                continue

            header = self._normalize(cell.value)

            headers[header] = cell.column

        row = 2

        while True:

            sr_no = self.ws.cell(
                row=row,
                column=headers["S. No."]
            ).value

            if sr_no is None:
                break

            if str(sr_no).strip().upper() == "TOTAL":
                break

            scores.append({

                "S. No.": self._cell(
                    row,
                    headers["S. No."]
                ),

                "Particulars": self._cell(
                    row,
                    headers["Particulars"]
                ),

                "Key Points": self._cell(
                    row,
                    headers["Key Points"]
                ),

                "Weightage": self._cell(
                    row,
                    headers["Weightage"]
                ),

                "Actual": self._cell(
                    row,
                    headers["Actual"]
                ),

                "Percentage": self._cell(
                    row,
                    headers["Percentage"]
                )

            })

            row += 1

        summary = self._extract_summary()

        return {
            "rows": scores,
            "summary": summary
        }

    def _normalize(self, text):

        text = str(text)

        text = text.replace("\n", " ")

        text = " ".join(text.split())

        return text.strip()

    def _cell(self, row, column):

        value = self.ws.cell(
            row=row,
            column=column
        ).value

        if value is None:
            return ""

        return str(value)
    
    def _extract_summary(self):

        summary = {
            "total_key_points": "",
            "total_weightage": "",
            "total_actual": "",
            "percentage": "",
            "final_rating": ""
        }

        for row in self.ws.iter_rows():

            # TOTAL row -> check Particulars column
            particulars = row[1].value if len(row) > 1 else None

            if particulars is not None:

                if str(particulars).strip().upper() == "TOTAL":

                    excel_row = row[1].row

                    summary["total_key_points"] = self._cell(excel_row, 3)
                    summary["total_weightage"] = self._cell(excel_row, 4)
                    summary["total_actual"] = self._cell(excel_row, 5)
                    summary["percentage"] = self._cell(excel_row, 6)

            # FINAL RATING row -> check first column
            first_cell = row[0].value

            if first_cell is not None:

                if str(first_cell).strip().upper() == "FINAL RATING":

                    excel_row = row[0].row

                    summary["final_rating"] = self._cell(excel_row, 6)

        return summary