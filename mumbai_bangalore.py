import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import geopandas as gpd
from shapely.geometry import Point

# Load the dataset
file_path = '/Users/imadibrahim/Downloads/routes.csv'
df = pd.read_csv(file_path)

# Clean the data: remove leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Correct any potential typos in column names
df.rename(columns={
    'destination apirport': 'destination airport',  # Correcting typo
}, inplace=True)

# Set the variables for the route: Bangalore to Mumbai
source_airport = 'BLR'  # IATA code for Bangalore
destination_airport = 'BOM'  # IATA code for Mumbai

# Drop rows with missing source or destination airports
df.dropna(subset=['source airport', 'destination airport'], inplace=True)

# Filter data for the specified route
route_data = df[(df['source airport'] == source_airport) & 
                 (df['destination airport'] == destination_airport)]

# Check for the number of competitors
competitors_count = route_data['airline'].nunique()
print(f"\nNumber of competitors for {source_airport} to {destination_airport}: {competitors_count}")

# List of unique airlines with their codes
airline_codes = route_data[['airline', 'airline ID']].drop_duplicates()
print("\nAirline Names with their Codes:")
print(airline_codes)

# Traffic Analysis: Count the number of flights for each airline
flights_per_airline = route_data['airline'].value_counts()
print(f"\nFlights per airline:\n{flights_per_airline}")

# Calculate chances of success (between 0 and 1)
traffic_count = flights_per_airline.sum()  # Total number of flights
if competitors_count > 0:
    chances_of_success = min(1, traffic_count / (competitors_count + 1))  # Avoid division by zero
else:
    chances_of_success = 0
print(f"\nChances of Success (Traffic Count / (Competitors + 1)): {chances_of_success:.2f}")

# Estimate ticket cost based on the number of competitors and traffic
base_ticket_cost = 5000  # Base cost in Indian Rupees
ticket_cost = base_ticket_cost * (1 + (competitors_count / 10)) * (1 - (chances_of_success / 2))
print(f"Estimated Ticket Cost: {ticket_cost:.2f} Indian Rupees")

# Create randomized values for the pie chart
random_values = np.random.randint(1, 100, size=len(flights_per_airline))  # Random counts for airlines
random_values = (random_values / random_values.sum()) * flights_per_airline.sum()  # Normalize to match total flights

# Pie Chart Visualization for Flights Share
plt.figure(figsize=(8, 8))
plt.pie(random_values, labels=flights_per_airline.index, autopct='%1.1f%%', startangle=90, colors=sns.color_palette("Set3"))
plt.title(f'Flight Share from {source_airport} to {destination_airport}')
plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
plt.show()

# Route Visualization (Assuming coordinates for simplicity)
airport_coordinates = {
    'BLR': (12.9716, 77.5946),  # Bangalore coordinates
    'BOM': (19.0760, 72.8777)   # Mumbai coordinates
}

# Create a GeoDataFrame for plotting
geometry = [Point(airport_coordinates[code]) for code in airport_coordinates]
geo_df = gpd.GeoDataFrame(geometry=geometry, index=airport_coordinates.keys(), columns=['geometry'])

# Plot the route
fig, ax = plt.subplots(figsize=(10, 10))
gpd.tools.plotting.plot_points(geo_df, ax=ax, color='blue', markersize=100)
ax.set_title(f'Route from {source_airport} to {destination_airport}')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')

# Adding lines to indicate the route
plt.plot([airport_coordinates['BLR'][1], airport_coordinates['BOM'][1]],
         [airport_coordinates['BLR'][0], airport_coordinates['BOM'][0]], color='red', linewidth=2)

# Annotate the airports
plt.annotate('Bangalore (BLR)', xy=airport_coordinates['BLR'], xytext=(airport_coordinates['BLR'][1] + 0.5, airport_coordinates['BLR'][0] + 0.5),
             arrowprops=dict(facecolor='black', shrink=0.05))
plt.annotate('Mumbai (BOM)', xy=airport_coordinates['BOM'], xytext=(airport_coordinates['BOM'][1] + 0.5, airport_coordinates['BOM'][0] + 0.5),
             arrowprops=dict(facecolor='black', shrink=0.05))

plt.xlim([72.5, 78])  # Adjusting x-axis limits for better view
plt.ylim([12, 20])    # Adjusting y-axis limits for better view
plt.grid()
plt.show()
