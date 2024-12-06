import src.process_incident_pdf  # Assuming the new code is saved as `project0/main.py`
import os
import sqlite3
import requests
import pytest


# Test for HTTP status code
def test_status_code():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-11/2024-11-02_daily_incident_summary.pdf"
    response = requests.get(url)
    assert response.status_code == 200, "The URL should return a 200 status code"