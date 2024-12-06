Here's a comprehensive README for the Norman PD Incident Data Visualizer project:

# Norman PD Incident Data Visualizer

This project provides a web-based visualization tool for Norman Police Department incident data. It allows users to download incident PDFs, process the data, and view various visualizations.

## Features

- Download and process incident PDFs
- Store incident data in a SQLite database
- Visualize incident data using:
  - Bar charts of incident counts by nature
  - Clustering of incidents by nature
  - Line charts showing incidents over time

## Demo 

[![Watch the video](https://lh3.googleusercontent.com/pw/AP1GczNlNM-FeNkXhuDQLX0aoj6SOHn5hwJVj3ufng5VCG_GyU-2LzzKP2JAE_Pf2T24LMBGYhPYfCO_ELt9aAupGMd8qDqsRVec8_XjsMP1EdWkdfk826RUagm9ac_DssHp79BiBWijyKSrkBKXJbAFGkbR0g=w1163-h653-s-no-gm?authuser=1)](https://youtu.be/oZTe2cs1M_0)
## Installation

1. Clone the repository:
   ```
   git clone https://github.com/archit0712/cis6930fa24-project3.git
   cd cis6930fa24-project3
   ```

2. Install dependencies using pipenv:
   ```
   pipenv install
   ```

## Usage

1. Activate the virtual environment:
   ```
   pipenv shell
   ```

2. Run the Streamlit app:
   ```
   pipenv run streamlit run src/app.py
   ```

3. Open your web browser and navigate to the URL provided by Streamlit (usually http://localhost:8501).

4. Enter the URL of a Norman PD incident PDF when prompted.

5. Use the radio buttons to switch between different visualization types.

## Code Structure

### process_incident_pdf.py

- `download_incident_pdf(url)`: Downloads the incident PDF from the given URL.
- `extract_incident_pdf_data(pdf_path)`: Extracts incident data from the PDF.
- `create_database(db_name)`: Creates an SQLite database to store incident data.
- `insert_incident_data(conn, incident)`: Inserts an incident record into the database.

### app.py

- `load_data(url)`: Downloads PDF, extracts data, and loads it into a DataFrame.
- `cluster_data(df, num_clusters)`: Performs K-means clustering on incident natures.
- `create_bar_chart(data)`: Creates a bar chart of incident counts by nature.
- `create_cluster_chart(df)`: Creates a scatter plot of clustered incidents.
- `create_cluster(df)`: Handles the clustering visualization process.
- `create_line_chart(data)`: Creates a line chart of incidents over time.
- `main()`: The main Streamlit application logic.

## Clustering Logic and Visualization Analysis

The clustering implementation uses five main categories to group incidents:

### Cluster 0 (Medical/Healthcare)
- Transfer/Interfacility
- Sick Person
- Medical-related incidents
- Logic: Groups medical emergencies requiring professional healthcare response

### Cluster 1 (General Incidents)
- Falls
- Alarms
- Welfare Checks
- Logic: Common incidents requiring routine police response

### Cluster 2 (Domestic/Disturbance)
- Disturbance/Domestic
- Family disputes
- Logic: Groups incidents involving domestic situations or disturbances

### Cluster 3 (Vehicle Accidents)
- MVA With Injuries
- MVA Non Injury
- Logic: Groups all motor vehicle accidents together

### Cluster 4 (Traffic)
- Traffic Stops
- Traffic violations
- Logic: Groups routine traffic enforcement activities

## Visualization Components

1. **Bar Chart**
   - Shows frequency of each incident type
   - X-axis: Nature of incident
   - Y-axis: Number of occurrences
   - Purpose: Quick identification of most common incident types

2. **Clustering Visualization**
   - Scatter plot showing incident groupings
   - X-axis: Cluster ID
   - Y-axis: Incident Nature
   - Color coding: Represents different clusters
   - Hover data: Location and timestamp
   - Purpose: Pattern recognition in incident types

3. **Line Chart**
   - Time-based visualization
   - X-axis: Time of day
   - Y-axis: Number of incidents
   - Purpose: Temporal pattern analysis

## Testing

To run the tests:

```
pipenv run python -m pytest
```

The test suite includes:
1. `test_download_incident_pdf`: Ensures PDFs can be downloaded successfully
2. `test_insert_incident_data`: Verifies correct data insertion into the database
3. `test_create_database`: Checks database creation functionality
4. `test_extract_incident_pdf_data`: Validates PDF data extraction
5. `test_status_code`: Confirms the incident PDF URL is accessible

## Dependencies

- streamlit
- pandas
- plotly
- scikit-learn
- requests
- pymupdf

## Notes

- Ensure you have a stable internet connection to download incident PDFs.
- The application requires write permissions in the directory it's run from to create and manage the SQLite database.




