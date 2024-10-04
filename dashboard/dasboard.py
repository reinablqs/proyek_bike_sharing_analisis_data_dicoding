import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os 

# Function to load data
def load_data(filename):
    # Get the directory of the current script file
    script_dir = os.path.dirname(__file__)  
    # Construct the full path to the CSV file in the same directory
    file_path = os.path.join(script_dir, filename)
    return pd.read_csv(file_path)

# Load both datasets
day_df = load_data('day_df.csv')
hour_df = load_data('hour_df.csv')

# Convert the 'dteday' column to datetime type if it's not already
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Extract years for selection
day_df['year'] = day_df['dteday'].dt.year
hour_df['year'] = hour_df['dteday'].dt.year

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Select a page", ["Day Data", "Hour Data"])

# Page 1: Day Data
if page == "Day Data":
    st.title("Jumlah Peminjaman Sepeda per Hari")
    
    # Year selection with "Select All" option
    years = day_df['year'].unique()
    years = sorted(years)  # Sort years for better user experience
    selected_year = st.selectbox("Select Year", ["Select All"] + list(years))

    # Filter the day_df based on the selected year
    if selected_year == "Select All":
        filtered_day_df = day_df  # Show all data if "Select All" is selected
    else:
        filtered_day_df = day_df[day_df['year'] == selected_year]

    # Visualisasi 
    
    st.header('Dashboard: Jumlah Peminjaman Sepeda Berdasarkan Cuaca dan Hari Kerja')

    # Group the data
    grouped_data = filtered_day_df.groupby(['weathersit', 'workingday'])['cnt'].sum().unstack()

    # Create a bar plot
    plt.figure(figsize=(12, 6))
    grouped_data.plot(kind='bar', ax=plt.gca())
    plt.title('Jumlah Peminjaman Sepeda Berdasarkan Cuaca dan Hari Kerja')
    plt.xlabel('Cuaca')
    plt.ylabel('Jumlah Peminjaman')
    plt.legend(labels=['Holiday', 'Weekday'])  # Adjust labels according to 'workingday' values
    plt.xticks(rotation=0)  # Rotate x-axis labels
    plt.tight_layout()  # Adjust layout

    # Display the plot in Streamlit
    st.pyplot(plt)

# Page 2: Hour Data
elif page == "Hour Data":
    st.title("Jumlah Peminjaman Sepeda per Jam")
    
    # Year selection with "Select All" option
    years_hour = hour_df['year'].unique()
    years_hour = sorted(years_hour)  # Sort years for better user experience
    selected_year_hour = st.selectbox("Select Year", ["Select All"] + list(years_hour))

    # Filter the hour_df based on the selected year
    if selected_year_hour == "Select All":
        filtered_hour_df = hour_df  # Show all data if "Select All" is selected
    else:
        filtered_hour_df = hour_df[hour_df['year'] == selected_year_hour]


    # Visualisasi 

    st.header('Rata-rata Peminjaman sepeda oleh pengguna casual dan registered Tiap Jam')

    # Group by hour and calculate the mean rentals for casual and registered users
    hourly_rentals = filtered_hour_df.groupby('hr')[['casual', 'registered']].mean().reset_index()

    # Create the plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='hr', y='casual', data=hourly_rentals, label='Casual Users', marker='o')
    sns.lineplot(x='hr', y='registered', data=hourly_rentals, label='Registered Users', marker='o')

    # Add titles and labels
    plt.title('Average Hourly Rentals for Casual and Registered Users')
    plt.xlabel('Hour of the Day')
    plt.ylabel('Average Number of Rentals')
    plt.legend()
    plt.xticks(range(0, 24))  # Set x-ticks from 0 to 23 to represent hours

    # Display the plot in Streamlit
    st.pyplot(plt)
