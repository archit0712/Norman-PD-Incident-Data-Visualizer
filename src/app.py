import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from process_incident_pdf import download_incident_pdf, extract_incident_pdf_data, create_database, insert_incident_data

# Function to load and process data from PDF URL
def load_data(url):
    pdf_path = download_incident_pdf(url)
    incident_records = extract_incident_pdf_data(pdf_path)
    
    with create_database('incidents.db') as conn:
        cursor = conn.cursor()
        # Clear existing data
        cursor.execute('DELETE FROM incidents')
        # Insert new data
        for incident in incident_records:
            insert_incident_data(conn, incident)
        # Fetch the data
        df = pd.read_sql_query("SELECT * FROM incidents", conn)
    
    return df
# Function to perform clustering on the 'Nature' column
def cluster_data(df, num_clusters=5):
    # Use TF-IDF to vectorize the 'Nature' column for text clustering
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['nature'])
    
    # Apply K-Means clustering
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    df['Cluster'] = kmeans.fit_predict(tfidf_matrix)
    
    return df
def create_bar_chart(data):
    fig = px.bar(data, x='Nature', y='Count', 
                 title='Incident Counts by Nature',
                 labels={'Nature': 'Incident Nature', 'Count': 'Number of Incidents'},
                 height=600)
    fig.update_xaxes(tickangle=45)
    return fig
# Function to create a scatter plot for clusters
def create_cluster_chart(df):
    fig = px.scatter(
        df,
        x="Cluster",
        y="nature",
        color="Cluster",
        title="Clustering of Incidents by Nature",
        labels={"Cluster": "Cluster ID", "nature": "Incident Nature"},
        hover_data=["location", "date_time"]
    )
    return fig

# Function to create a clustering
def create_cluster(df):
     # Sidebar for cluster configuration
        st.sidebar.header("Clustering Configuration")
        num_clusters = st.sidebar.slider("Number of Clusters", min_value=2, max_value=10, value=5)
        
        # Perform clustering
        clustered_df = cluster_data(df, num_clusters=num_clusters)
        
        # Display clustered data table
        st.subheader("Clustered Data")
        st.dataframe(clustered_df[['date_time', 'location', 'nature', 'Cluster']])
        
        # Create and display cluster chart
        st.subheader("Clustering Visualization")
        cluster_chart = create_cluster_chart(clustered_df)
        st.plotly_chart(cluster_chart)
        
def create_line_chart(data):
    data['date_time'] = pd.to_datetime(data['date_time'], errors='coerce')
    data_grouped = data.groupby(pd.Grouper(key='date_time', freq='H')).size().reset_index(name='Count')
    fig = px.line(data_grouped, x='date_time', y='Count', 
                  title='Incidents Over Time',
                  labels={'date_time': 'Date/Time', 'Count': 'Number of Incidents'})
    return fig
# Main Streamlit app function
def main():
    st.title("Norman PD Incident Data Visualizer")

    url = st.text_input("Enter the URL of the incident PDF:")
    if url:
        df = load_data(url)
        # Count incidents by nature for bar and Clusterings
        nature_counts = df['nature'].value_counts().reset_index()
        nature_counts.columns = ['Nature', 'Count']
        
        # Chart selection toggle
        chart_type = st.radio(
            "Select Chart Type:",
            ('Bar Chart', 'Clustering', 'Line Chart')
        )

        if chart_type == 'Bar Chart':
            st.subheader("Incident Counts by Nature")
            bar_fig = create_bar_chart(nature_counts)
            st.plotly_chart(bar_fig)
            
        elif chart_type == 'Clustering':
                st.subheader("Incident Distribution by Nature")
                create_cluster(df)
                

        elif chart_type == 'Line Chart':
            st.subheader("Incidents Over Time")
            line_fig = create_line_chart(df)
            st.plotly_chart(line_fig)    
       
        
if __name__ == "__main__":
    main()