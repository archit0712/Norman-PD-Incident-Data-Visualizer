import src.process_incident_pdf  # Assuming the new code is saved as `project0/main.py`
import os
import sqlite3
import requests
import pytest


# Test for extracting PDF data and verifying correct format
def test_extract_incident_pdf_data():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-11/2024-11-02_daily_incident_summary.pdf"
    pdf_path = src.process_incident_pdf.download_incident_pdf(url)
    
    incidents = src.process_incident_pdf.extract_incident_pdf_data(pdf_path)
    assert len(incidents) > 0, "There should be incidents extracted from the PDF"
    assert 'date_time' in incidents[0], "Incident data should contain 'date_time'"
    assert 'incident_number' in incidents[0], "Incident data should contain 'incident_number'"
