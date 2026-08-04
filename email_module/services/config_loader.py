"""
config_loader.py

Loads and validates client configuration files.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, Any


class ConfigLoader:
    """
    Loads JSON configuration for a client.
    """

    REQUIRED_KEYS = [
        "client",
        "sheets",
        "audit_details",
        "checklist",
        "score_parameters",
        "email"
    ]

    def __init__(self, config_directory: str | Path = "configs") -> None:
        """
        Initializes the ConfigLoader. Forces relative paths to anchor 
        to the email_module directory to prevent pathing issues.
        """
        provided_path = Path(config_directory)
        
        if provided_path.is_absolute():
            # If an absolute path is provided, trust it
            self.config_directory = provided_path
        else:
            # Force the path to resolve inside the email_module folder
            # __file__ is email_module/services/config_loader.py
            current_script_path = Path(__file__).resolve()
            
            # .parent.parent moves up to the email_module root
            # .name extracts just the folder name (e.g., "configs")
            self.config_directory = current_script_path.parent.parent / provided_path.name

    def load(self, client: str) -> Dict[str, Any]:
        """
        Load client configuration.

        Example:
            loader.load("tata_capital")
        """

        config_file = self.config_directory / f"{client}.json"

        if not config_file.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_file}"
            )

        with open(config_file, "r", encoding="utf-8") as file:
            config = json.load(file)

        self._validate(config)

        return config

    def available_clients(self) -> list[str]:
        """
        Returns all available configuration names.
        """

        clients = []

        for file in self.config_directory.glob("*.json"):
            clients.append(file.stem)

        clients.sort()

        return clients

    def _validate(self, config: Dict[str, Any]) -> None:
        """
        Validate required configuration keys.
        """

        missing = []

        for key in self.REQUIRED_KEYS:

            if key not in config:
                missing.append(key)

        if missing:
            raise ValueError(
                f"Missing configuration keys: {', '.join(missing)}"
            )