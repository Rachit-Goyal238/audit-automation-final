"""
Extracts audit header information from the Checklist sheet.
"""

from email_module.models.audit_details import AuditDetails


class AuditDetailsExtractor:

    def __init__(self, worksheet, config):
        self.ws = worksheet
        self.config = config

    def extract(self) -> AuditDetails:

        cells = self.config["audit_details"]

        return AuditDetails(
            agency_code=self._value(cells["Agency Code"]),
            agency_name=self._value(cells["Agency Name"]),
            agency_address=self._value(cells["Agency Address"]),
            agency_type=self._value(cells["Type of Agency"]),
            auditor_name=self._value(cells["Auditor Name"]),
            audit_date=str(self._value(cells["Audit Date"])),
            collection_manager=self._value(cells["Collection Manager"]),
            agency_manager=self._value(cells["Agency Manager"])
        )

    def _value(self, cell_reference):

        value = self.ws[cell_reference].value

        if value is None:
            return ""

        return str(value).strip()