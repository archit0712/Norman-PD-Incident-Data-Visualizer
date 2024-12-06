import src.process_incident_pdf  # Assuming the new code is saved as `project0/main.py`
import os
import sqlite3
import requests
import pytest



# Test for inserting data into the database
def test_insert_incident_data():
    # Mock the incident data
    mock_incident = {
        'date_time': '09/08/2024 12:00',
        'incident_number': '123456',
        'location': 'Main St',
        'nature': 'Fire',
        'incident_ori': 'NORMAN'
    }
    
    conn = src.process_incident_pdf.create_database('test_incidents.db')  # Create test database
    src.process_incident_pdf.insert_incident_data(conn, mock_incident)
    
    # Verify that the data has been inserted correctly
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM incidents;")
    result = cursor.fetchall()
    
    assert len(result) == 1, "One incident should be inserted"
    assert result[0][1:] == ('09/08/2024 12:00', '123456', 'Main St', 'Fire', 'NORMAN'), "The inserted data should match the mock incident"
    
    cursor.execute("DROP TABLE incidents;")
    conn.close()
 