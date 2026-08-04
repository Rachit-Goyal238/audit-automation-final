"""
audit_details.py

Data model representing audit header information.
"""

from dataclasses import dataclass


@dataclass
class AuditDetails:
    agency_code: str
    agency_name: str
    agency_address: str
    agency_type: str
    auditor_name: str
    audit_date: str
    collection_manager: str
    agency_manager: str