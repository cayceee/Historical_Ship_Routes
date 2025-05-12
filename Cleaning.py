'''import pandas as pd

# Load the ship data
df = pd.read_csv("New_England_Processed.csv")

# Combine Origin and DestinationDecl into one Series, drop missing values
all_ports = pd.concat([df['Origin'], df['DestinationDecl']]).dropna()

# Get the 50 most common ports
top_ports = all_ports.value_counts().head(50).index.tolist()

# Load the geocoded locations
geo_df = pd.read_csv("geocoded_locations_clean.csv")

# Filter to only the top 50 ports
filtered_geo_df = geo_df[geo_df['Location'].isin(top_ports)]

# Save to a new CSV
filtered_geo_df.to_csv("top_50_geocoded_locations.csv", index=False)

print("✅ Saved top 50 geocoded locations to top_50_geocoded_locations.csv")

print(filtered_geo_df['Location'])
'''
####################

import pandas as pd

# Load your data
shipData = pd.read_csv("New_England_Processed.csv")

# List of top 50 geocoded locations (replace this with your actual list)
top_50_geocoded_locations = [
    'Savannah', 'Boston', 'Norfolk', 'Cape Francoise', 'New York', 'Martinico', 'Demerara', 
    'Philadelphia', 'Alexandria', 'London', 'Antigua', 'Amsterdam', 'Portsmouth', 'Barbadoes', 
    'Salem', 'Portland', 'Lisbon', 'Bourdeaux', 'Madeira', 'St. Croix', 'Trinadad', 'Liverpool', 
    'Richmond', 'Greenock', 'Cadiz', 'Jamaica', 'St. Johns', 'Havana', 'West-Indies', 'Baltimore', 
    'Charleston', 'New Bedford', 'St. Thomas', 'Wilmington', 'Tobago', 'Rotterdam', 'Halifax', 
    'Guadaloupe', 'New Orleans', 'Windsor', 'Plymouth', 'Yarmouth', 'Trinidad', 'New Haven', 
    'New London', 'Gloucester', 'Newbern', 'Martinique'
]

# Filter the ship data to only include rows where both Origin and DestinationDecl are in top_50_geocoded_locations
filtered_ship_data = shipData[
    shipData['Origin'].isin(top_50_geocoded_locations) & 
    shipData['DestinationDecl'].isin(top_50_geocoded_locations)
]

# Check the filtered data
print(filtered_ship_data)

# You can save the filtered data if needed
filtered_ship_data.to_csv("Filtered_New_England_Processed.csv", index=False)
