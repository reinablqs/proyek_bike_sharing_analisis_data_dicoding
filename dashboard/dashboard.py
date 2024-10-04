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
    st.title("Daily Rental Bike")
    
    # Year selection with "Select All" option
    years = day_df['year'].unique()
    years = sorted(years)  # Sort years for better user experience
    selected_year = st.selectbox("Select Year", ["Select All"] + list(years))

    # Filter the day_df based on the selected year
    if selected_year == "Select All":
        filtered_day_df = day_df  # Show all data if "Select All" is selected
    else:
        filtered_day_df = day_df[day_df['year'] == selected_year]

    # Visualisasi 1
    
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


    st.header('Average Daily Rentals for Casual and Registered Users')

    # Group by hour and calculate the mean rentals for casual and registered users
    hourly_rentals = filtered_day_df.groupby('hr')[['casual', 'registered']].mean().reset_index()

    # Create the plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='hr', y='casual', data=hourly_rentals, label='Casual Users', marker='o')
    sns.lineplot(x='hr', y='registered', data=hourly_rentals, label='Registered Users', marker='o')

    # Add titles and labels
    plt.title('Average Daily Rentals for Casual and Registered Users')
    plt.xlabel('Day of the Week')
    plt.ylabel('Average Number of Rentals')
    plt.legend()
    plt.xticks(range(0, 24))  # Set x-ticks from 0 to 23 to represent hours

    # Display the plot in Streamlit
    st.pyplot(plt)

    # Visualisasi 2 

    # Group by days_of_the_week and calculate the mean rentals for casual and registered users
    daily_rentals = day_df.groupby('days_of_the_week')[['casual', 'registered']].mean().reset_index()

    # Mengurutkan hari dalam seminggu (Senin hingga Minggu)
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    daily_rentals['days_of_the_week'] = pd.Categorical(daily_rentals['days_of_the_week'], categories=days_order, ordered=True)
    daily_rentals = daily_rentals.sort_values('days_of_the_week')

    # Create the plot
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='days_of_the_week', y='casual', data=daily_rentals, label='Casual Users', marker='o')
    sns.lineplot(x='days_of_the_week', y='registered', data=daily_rentals, label='Registered Users', marker='o')

    # Add titles and labels
    plt.title('Average Daily Rentals for Casual and Registered Users')
    plt.xlabel('Days of the Week')
    plt.ylabel('Average Number of Rentals')
    plt.legend()

    # Show the plot
    st.pyplot(plt)


# Page 2: Hour Data
elif page == "Hour Data":
    st.title("Hourly Rental Bike")
    
    # Year selection with "Select All" option
    years_hour = hour_df['year'].unique()
    years_hour = sorted(years_hour)  # Sort years for better user experience
    selected_year_hour = st.selectbox("Select Year", ["Select All"] + list(years_hour))

    # Filter the hour_df based on the selected year
    if selected_year_hour == "Select All":
        filtered_hour_df = hour_df  # Show all data if "Select All" is selected
    else:
        filtered_hour_df = hour_df[hour_df['year'] == selected_year_hour]


    # Visualisasi 1

    st.header('Average Hourly Rentals for Casual and Registered Users')

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

    # Visualisasi 2 

    # Grouping data berdasarkan 'temp_category' dan 'workingday', lalu menghitung total peminjaman ('cnt')
    grouped_data = hour_df.groupby(['temp_category', 'workingday'])['cnt'].sum().unstack()

    # Membuat plot bar
    ax = grouped_data.plot(kind='bar', figsize=(12, 6))

    # Menambahkan angka jumlah peminjaman pada setiap bar
    for p in ax.containers:
        ax.bar_label(p, label_type='edge')  # Menampilkan angka di atas setiap bar

    # Menambahkan judul dan label
    plt.title('Number of Bikes Borrowed Based on Temperature Category and Working Day')
    plt.xlabel('Temperature Category')
    plt.ylabel('Sum of Rentals')
    plt.legend(labels=['Holiday', 'Weekday'])  # Ubah label sesuai dengan nilai di kolom working day
    plt.xticks(rotation=0)  # Mengatur posisi label di sumbu x agar tidak miring
    plt.tight_layout()  # Mengatur layout agar elemen grafik tidak saling bertumpukan

    # Tampilkan grafik
    st.pyplot(plt)

