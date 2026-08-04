"""
table_html.py

Builds HTML tables for the email body.
"""
import math

class TableHTMLBuilder:

    BLUE = "#4F81BD"
    BORDER = "#000000"

    TABLE_STYLE = """
        width:700px;
        max-width:700px;
        margin:15px 0;
        border-collapse:collapse;
        table-layout:fixed;
        font-family:Calibri, Arial, sans-serif;
        font-size:13px;
    """
    TABLE_STYLE_1 = """
            width:600px;
            max-width:600px;
            margin:15px 0;
            border-collapse:collapse;
            table-layout:fixed;
            font-family:Calibri, Arial, sans-serif;
            font-size:13px;
        """
    TABLE_STYLE_2 = """
            width:900px;
            max-width:900px;
            margin:15px 0;
            border-collapse:collapse;
            table-layout:fixed;
            font-family:Calibri, Arial, sans-serif;
            font-size:13px;
        """
    def build_audit_table(self, details):

        html = f"""
        <table style="{self.TABLE_STYLE}">

        """

        rows = [

            ("Agency Code", details.agency_code,
            "Auditor Name", details.auditor_name),

            ("Agency Name", details.agency_name,
            "Audit Date", details.audit_date),

            ("Agency Address", details.agency_address,
            "Collection Manager", details.collection_manager),

            ("Type of Agency", details.agency_type,
            "Agency Manager", details.agency_manager)

        ]

        for left_label, left_value, right_label, right_value in rows:

            html += f"""

            <tr>

                <td style="
                    background:{self.BLUE};
                    color:white;
                    font-weight:bold;
                    border:1px solid {self.BORDER};
                    padding:8px;
                    width:17%;
                    vertical-align:top;
                    word-break:break-word;
                    font-size:13px;
                ">
                    {left_label}
                </td>

                <td style="
                    border:1px solid {self.BORDER};
                    padding:8px;
                    width:33%;
                    background:white;
                    white-space:normal;
                    word-break:break-word;
                    overflow-wrap:break-word;
                    vertical-align:top;
                    font-size:13px;
                ">
                    {left_value}
                </td>

                <td style="
                    background:{self.BLUE};
                    color:white;
                    font-weight:bold;
                    border:1px solid {self.BORDER};
                    padding:8px;
                    width:17%;
                    vertical-align:top;
                    word-break:break-word;
                    font-size:13px;
                ">
                    {right_label}
                </td>

                <td style="
                    border:1px solid {self.BORDER};
                    padding:8px;
                    width:33%;
                    background:white;
                    white-space:normal;
                    word-break:break-word;
                    overflow-wrap:break-word;
                    vertical-align:top;
                    font-size:13px;
                ">
                    {right_value}
                </td>

            </tr>
            """

        html += "</table>"

        return html

    def build_observations_table(self, observations):

        html = f"""
        <table style="{self.TABLE_STYLE_2}">

            <tr>

                <th style="{self._header_style()} width:14%;">
                    Rating Category
                </th>

                <th style="{self._header_style()} width:24%;">
                    Short Segmentation
                </th>

                <th style="{self._header_style()} width:46%;">
                    Observation
                </th>

                <th style="{self._header_style()} width:16%; text-align:center;">
                    Pending Status<br>(Open/Closed)
                </th>

            </tr>
        """

        for obs in observations:

            html += f"""

            <tr>

                <td style="{self._cell_style()}">
                    {obs.rating_category}
                </td>

                <td style="{self._cell_style()}">
                    {obs.short_segmentation}
                </td>

                <td style="{self._cell_style()}">
                    {str(obs.observation).replace(chr(10), "<br>")}
                </td>

                <td style="{self._cell_style()} text-align:center;">
                    {obs.pending_status}
                </td>

            </tr>

            """

        html += "</table>"

        return html

    def build_score_table(self, score_data):

        scores = score_data["rows"]
        summary = score_data["summary"]

        html = f"""
        <table style="{self.TABLE_STYLE_1}">

        <tr>

        <th style="{self._header_style()} width:8%; text-align:center;">S. No.</th>

        <th style="{self._header_style()} width:32%;">Particulars</th>

        <th style="{self._header_style()} width:15%; text-align:center;">Key Points</th>

        <th style="{self._header_style()} width:15%; text-align:center;">Weightage</th>

        <th style="{self._header_style()} width:15%; text-align:center;">Actual</th>

        <th style="{self._header_style()} width:15%; text-align:center;">Percentage</th>

        </tr>
        """

        for row in scores:

            percentage = row.get("Percentage", "")

            try:
                percentage = float(percentage)

                if percentage <= 1:
                    percentage *= 100

                percentage = f"{int(percentage + 0.5)}%"

            except (ValueError, TypeError):
                pass

            html += f"""
            <tr>

            <td style="{self._cell_style()} text-align:center;">
            {row["S. No."]}
            </td>

            <td style="{self._cell_style()}">
            {row["Particulars"]}
            </td>

            <td style="{self._cell_style()} text-align:center;">
            {row["Key Points"]}
            </td>

            <td style="{self._cell_style()} text-align:center;">
            {row["Weightage"]}
            </td>

            <td style="{self._cell_style()} text-align:center;">
            {row["Actual"]}
            </td>

            <td style="{self._cell_style()} text-align:center;">
            {percentage}
            </td>

            </tr>
            """

        total_percentage = summary.get("percentage", "")

        try:
            total_percentage = float(total_percentage)

            if total_percentage <= 1:
                total_percentage *= 100

            total_percentage = int(total_percentage + 0.5)

        except (ValueError, TypeError):
            total_percentage = 0

        display_percentage = f"{total_percentage}%"

        # Percentage cell colour
        if total_percentage >= 80:
            total_bg = "#A9D18E"      # A - Green
            total_fg = "#000000"
        elif total_percentage >= 70:
            total_bg = "#FFC000"      # B - Orange/Gold
            total_fg = "#000000"
        elif total_percentage >= 60:
            total_bg = "#FFC000"      # C - Yellow
            total_fg = "#000000"
        elif total_percentage >= 50:
            total_bg = "#FF0000"      # D - Light Red
            total_fg = "#000000"
        else:
            total_bg = "#FF0000"      # E - Red
            total_fg = "#FFFFFF"

        html += f"""
        <tr>

            <!-- Blank S.No. cell -->
            <td style="
                border:1px solid {self.BORDER};
                padding:4px;
                background:white;
            ">
            </td>

            <!-- Total -->
            <td style="
                background:{self.BLUE};
                color:white;
                font-weight:bold;
                border:1px solid {self.BORDER};
                padding:4px;
                text-align:center;
            ">
                Total
            </td>

            <!-- Key Points -->
            <td style="
                background:{self.BLUE};
                color:white;
                font-weight:bold;
                border:1px solid {self.BORDER};
                padding:4px;
                text-align:center;
            ">
                {summary.get("total_key_points", "")}
            </td>

            <!-- Weightage -->
            <td style="
                background:{self.BLUE};
                color:white;
                font-weight:bold;
                border:1px solid {self.BORDER};
                padding:4px;
                text-align:center;
            ">
                {summary.get("total_weightage", "")}
            </td>

            <!-- Actual -->
            <td style="
                background:{self.BLUE};
                color:white;
                font-weight:bold;
                border:1px solid {self.BORDER};
                padding:4px;
                text-align:center;
            ">
                {summary.get("total_actual", "")}
            </td>

            <!-- Percentage -->
            <td style="
                background:{total_bg};
                color:{total_fg};
                font-weight:bold;
                border:1px solid {self.BORDER};
                padding:4px;
                text-align:center;
            ">
                {display_percentage}
            </td>

        </tr>

            <td colspan="5" style="
                background:{self.BLUE};
                color:white;
                font-weight:bold;
                border:1px solid {self.BORDER};
                padding:4px;
                text-align:center;
            ">
                FINAL RATING
            </td>

            <td style="
                background:{self.BLUE};
                color:white;
                font-weight:bold;
                border:1px solid {self.BORDER};
                padding:4px;
                text-align:center;
            ">
                {summary.get("final_rating", "")}
            </td>

        </tr>
        """

        html += "</table>"

        return html
    def _label_style(self):

        return f"""
        background:{self.BLUE};
        color:white;
        font-weight:bold;
        border:1px solid {self.BORDER};
        padding:6px 8px;
        width:17%;
        vertical-align:top;
        word-break:break-word;
        """

    def _value_style(self):

        return f"""
        border:1px solid {self.BORDER};
        padding:6px 8px;
        width:33%;
        vertical-align:top;
        white-space:normal;
        word-break:break-word;
        overflow-wrap:break-word;
        background:white;
        """

    def _header_style(self):

        return f"""
        background:{self.BLUE};
        color:white;
        border:1px solid {self.BORDER};
        padding:7px 8px;
        font-weight:bold;
        text-align:left;
        vertical-align:middle;
        font-size:13px;
        line-height:1.3;
        """


    def _cell_style(self):

        return f"""
        border:1px solid {self.BORDER};
        padding:6px 8px;
        vertical-align:top;
        background:white;
        white-space:normal;
        word-break:break-word;
        overflow-wrap:break-word;
        line-height:1.35;
        font-size:13px;
        """