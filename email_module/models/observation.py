"""
observation.py

Represents one observation that will appear in the email.
"""

from dataclasses import dataclass


@dataclass
class Observation:
    rating_category: str
    short_segmentation: str
    observation: str
    pending_status: str