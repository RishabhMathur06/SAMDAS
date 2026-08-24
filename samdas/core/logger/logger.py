# Imports dependencies.
import logging
import json
import os
import datetime

# Ensures the log direcotry exists.
os.makedirs("logs", exist_ok=True)

class JSONFormatter(logging.Formatter):
    """
        Custom JSON formatter for Enterprise logging
    """
    def format(self, record):
        log_obj = {
            "timestamp": datetime.datetime.now().isoformat(),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage()
        }

        return json.dumps(log_obj)

# Creates Custom SAMDAS logger.
firewall_logger = logging.getLogger("SAMDAS_FIREWALL")
firewall_logger.setLevel(logging.INFO)

# Prevents the logger from duplicating messages if imported multiple times.
if not firewall_logger.handlers:
    # File handler (JSONL Format).
    file_handler = logging.FileHandler("logs/samdas_firewall.jsonl")
    file_handler.setFormatter(JSONFormatter())
    firewall_logger.addHandler(file_handler)

    # Console Handler (Standard Format).
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("[%(levelname)s] (%(module)s) %(message)s")
    console_handler.setFormatter(console_formatter)
    firewall_logger.addHandler(console_handler)