import pandas as pd
import time
from geopy.geocoders import Nominatim
from tqdm import tqdm

# Load the original ship data
df = pd.read_csv("New_England_Processed.csv")

# Combine and get unique location names from both origin and destination
original_locations = pd.Series(df['Origin'].tolist() + df['DestinationDecl'].tolist()).dropna().unique()

# Dictionary of ambiguous names mapped to more precise, major-port versions (used only for geocoding)
replacements = {
    'Norfolk': 'Norfolk, Virginia, United States',
    'Gibraltar': 'Gibraltar, British Overseas Territory',
    'Petersburg': 'Petersburg, Virginia, United States',
    'Boston': 'Boston, Massachusetts, United States',
    'Marseilles': 'Marseille, Provence-Alpes-Côte d\'Azur, France',
    'Falmouth': 'Falmouth, Cornwall, United Kingdom',
    'New York': 'New York, New York, United States',
    'Savannah': 'Savannah, Georgia, United States',
    'Rouen': 'Rouen, Normandy, France',
    'Liverpool': 'Liverpool, England, United Kingdom',
    'London': 'London, England, United Kingdom',
    'Málaga': 'Málaga, Andalusia, Spain',
    'Cape Francoise': 'Cap-Haïtien, Haiti',
    'Isle of France': 'Port Louis, Mauritius',
    'Gibraltar': 'Gibraltar, Gibraltar',
    'Salem': 'Salem, Massachusetts, United States',
    'West-Indies': 'Caribbean',
    'Alexandria': 'Alexandria, Egypt',
    'Portland': 'Portland, Maine, United States',
    'Cadiz': 'Cadiz, Spain',
    'St. Johns': 'St. Johns, Newfoundland, Canada',
    'Newbern': 'Newbern, North Carolina, United States',
    'Gloucester': 'Gloucester, United Kingdom',
    
}

# Set up geocoder
geolocator = Nominatim(user_agent="ship-route-demo")

# Geocode each location with fallback to replacement
coordinates = []
for loc in tqdm(original_locations, desc="Geocoding locations"):
    query = replacements.get(loc, loc)
    try:
        geocoded = geolocator.geocode(query)
        if geocoded:
            coordinates.append({'Location': loc, 'Latitude': geocoded.latitude, 'Longitude': geocoded.longitude})
        else:
            coordinates.append({'Location': loc, 'Latitude': None, 'Longitude': None})
    except Exception:
        coordinates.append({'Location': loc, 'Latitude': None, 'Longitude': None})
    time.sleep(1)  # Respect Nominatim's rate limit

# Save geocoded results (original names retained)
geo_df = pd.DataFrame(coordinates)
geo_df.to_csv("geocoded_locations.csv", index=False)

# Save clean version without missing coordinates
geo_df_clean = geo_df.dropna(subset=["Latitude", "Longitude"])
geo_df_clean.to_csv("geocoded_locations_clean.csv", index=False)

print("✅ Geocoding complete and files saved.")
