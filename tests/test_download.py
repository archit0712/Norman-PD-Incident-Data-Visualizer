import src.process_incident_pdf  # Assuming the new code is saved as `project0/main.py`
import os

# Test for downloading PDF from the URL
def test_download_incident_pdf():
    url = "https://www.normanok.gov/sites/default/files/documents/2024-11/2024-11-02_daily_incident_summary.pdf"
    pdf_path = src.process_incident_pdf.download_incident_pdf(url)
    assert pdf_path is not None, "PDF should be downloaded successfully"
    assert os.path.exists(pdf_path), "The PDF file should exist in the resources folder"

   




