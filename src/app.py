import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA
import numpy as np
from process_incident_pdf import download_incident_pdf, extract_incident_pdf_data, create_database, insert_incident_data
def load_data(url):
    pdf_path = download_incident_pdf(url)
    incident_records = extract_incident_pdf_data(pdf_path)
    
    with create_database('incidents.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM incidents')
        for incident in incident_records:
            insert_incident_data(conn, incident)
        df = pd.read_sql_query("SELECT * FROM incidents", conn)
    return df

def improved_cluster_data(df, n_clusters=8):
    # Text preprocessing and vectorization
    vectorizer = TfidfVectorizer(
        stop_words='english',
        max_features=100,
        ngram_range=(1, 2)
    )
    tfidf_matrix = vectorizer.fit_transform(df['nature'])
    
    # Dimension reduction
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(tfidf_matrix.toarray())
    
    # Hierarchical clustering
    clustering = AgglomerativeClustering(
        n_clusters=n_clusters,
        linkage='ward'
    )
    df['Cluster'] = clustering.fit_predict(reduced_features)
    
    # Add PCA components for visualization
    df['PCA1'] = reduced_features[:, 0]
    df['PCA2'] = reduced_features[:, 1]
    
    return df

def create_cluster_chart(df):
    fig = px.scatter(
        df,
        x='PCA1',
        y='PCA2',
        color='Cluster',
        hover_data=['nature', 'location', 'date_time'],
        title='Clustering of Incidents by Nature',
        labels={
            'PCA1': 'First Principal Component',
            'PCA2': 'Second Principal Component',
            'Cluster': 'Incident Cluster'
        }
    )
    fig.update_layout(height=600)
    return fig

def create_bar_chart(data):
    fig = px.bar(
        data, 
        x='Nature', 
        y='Count',
        title='Incident Counts by Nature',
        labels={'Nature': 'Incident Nature', 'Count': 'Number of Incidents'},
        height=600
    )
    fig.update_xaxes(tickangle=45)
    return fig

def create_line_chart(data):
    data['date_time'] = pd.to_datetime(data['date_time'])
    data_grouped = data.groupby(
        pd.Grouper(key='date_time', freq='H')
    ).size().reset_index(name='Count')
    
    fig = px.line(
        data_grouped, 
        x='date_time', 
        y='Count',
        title='Incidents Over Time',
        labels={'date_time': 'Date/Time', 'Count': 'Number of Incidents'}
    )
    return fig

def main():
    st.title("Norman PD Incident Data Visualizer")
    
    url = st.text_input("Enter the URL of the incident PDF:")
    if url:
        df = load_data(url)
        
        # Chart selection
        chart_type = st.radio(
            "Select Chart Type:",
            ('Bar Chart', 'Clustering', 'Line Chart')
        )
        
        if chart_type == 'Bar Chart':
            nature_counts = df['nature'].value_counts().reset_index()
            nature_counts.columns = ['Nature', 'Count']
            st.plotly_chart(create_bar_chart(nature_counts))
            
        elif chart_type == 'Clustering':
            st.sidebar.header("Clustering Configuration")
            n_clusters = st.sidebar.slider(
                "Number of Clusters",
                min_value=2,
                max_value=10,
                value=5
            )
            
            clustered_df = improved_cluster_data(df, n_clusters)
            st.dataframe(
                clustered_df[['date_time', 'location', 'nature', 'Cluster']]
            )
            st.plotly_chart(create_cluster_chart(clustered_df))
            
        elif chart_type == 'Line Chart':
            st.plotly_chart(create_line_chart(df))

if __name__ == "__main__":
    main()