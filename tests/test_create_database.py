import src.process_incident_pdf
import os
import sqlite3
import requests
import pytest


# Test for database creation
def test_create_database():
    conn = src.process_incident_pdf.create_database('test_incidents.db')
    assert conn is not None, "Database connection should be established"
    
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='incidents';")
    result = cursor.fetchone()
    assert result is not None, "The 'incidents' table should be created"
    
    cursor.execute("DROP TABLE incidents;")
    conn.close()