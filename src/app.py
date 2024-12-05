import streamlit as st
import pandas as pd
import plotly.express as px
from process_incident_pdf import download_incident_pdf, extract_incident_pdf_data, create_database, insert_incident_data

def load_data(url):
    pdf_path = download_incident_pdf(url)
    incident_records = extract_incident_pdf_data(pdf_path)
    
    conn = create_database('incidents.db')
    for incident in incident_records:
        insert_incident_data(conn, incident)
    
    df = pd.read_sql_query("SELECT * FROM incidents", conn)
    conn.close()
    return df

def create_bar_chart(data):
    fig = px.bar(data, x='Nature', y='Count', 
                 title='Incident Counts by Nature',
                 labels={'Nature': 'Incident Nature', 'Count': 'Number of Incidents'},
                 height=600)
    fig.update_xaxes(tickangle=45)
    return fig

def main():
    st.title("Norman PD Incident Data Visualizer")

    url = st.text_input("Enter the URL of the incident PDF:")
    if url:
        df = load_data(url)
        
        nature_counts = df['nature'].value_counts().reset_index()
        nature_counts.columns = ['Nature', 'Count']
        
        st.subheader("Incident Counts by Nature")
        fig = create_bar_chart(nature_counts)
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()