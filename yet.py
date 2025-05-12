'''import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from geopy.geocoders import Nominatim


testing = pd.DataFrame({
    'Ship Name': ['Dispatch', 'Rufus', 'Polly', 'Ocean', 'Hannah', 'Two Brothers', 'Susan', 'Patty', 'Polly', 'THE_RONZOR'],
    'Origin': ['Savannah', 'Savannah', 'Petersburg', 'Isle of France', 'Boston', 'Boston', 'Málaga, Spain', 'Norfolk', 'Cape Francoise', 'London'],
    'Declared Destination': ['Boston', 'Liverpool', 'Boston', 'Boston', 'St. Croix', 'Falmouth', 'Rouen', 'Marseilles', 'New York', 'Savannah']
})


geolocator = Nominatim(user_agent="ship-route-demo")


def get_coordinates(city_name):
    try:
        location = geolocator.geocode(city_name)
        return (location.latitude, location.longitude) if location else (None, None)
    except:
        return (None, None)


testing['Origin Lat'], testing['Origin Lon'] = zip(*testing['Origin'].map(get_coordinates))
testing['Dest Lat'], testing['Dest Lon'] = zip(*testing['Declared Destination'].map(get_coordinates))


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Ship Route Visualizer", style={'textAlign': 'center'}),

    html.Label("Select Ship:"),
    dcc.Dropdown(
        id='ship-dropdown',
        options=[{'label': name, 'value': name} for name in testing['Ship Name']],
        value='Neptune'
    ),

    dcc.Graph(id='route-map', style={'marginTop': 30})
])

@app.callback(
    Output('route-map', 'figure'),
    Input('ship-dropdown', 'value')
)
def update_map(ship_name):
    ship_row = testing[testing['Ship Name'] == ship_name].iloc[0]

    fig = go.Figure()

    # Draw the line
    fig.add_trace(go.Scattergeo(
        lon=[ship_row['Origin Lon'], ship_row['Dest Lon']],
        lat=[ship_row['Origin Lat'], ship_row['Dest Lat']],
        mode='lines+markers',
        line=dict(width=2, color='blue'),
        marker=dict(size=6, color='blue'),
        name=f"{ship_row['Ship Name']} Route"
    ))

    # Add arrowhead using a triangle-up marker at the destination
    fig.add_trace(go.Scattergeo(
        lon=[ship_row['Dest Lon']],
        lat=[ship_row['Dest Lat']],
        mode='markers',
        marker=dict(
            size=12,
            symbol='triangle-up',
            color='blue',
            angle=0  # Note: angle is not supported in scattergeo, so arrowhead will always point up
        ),
        name='Destination (Arrowhead)'
    ))

    origin_lon, origin_lat = ship_row['Origin Lon'], ship_row['Origin Lat']
    dest_lon, dest_lat = ship_row['Dest Lon'], ship_row['Dest Lat']

    # Dynamically set the longitude and latitude ranges based on the origin and destination
    lon_range = [min(origin_lon, dest_lon) - 10, max(origin_lon, dest_lon) + 10]
    lat_range = [min(origin_lat, dest_lat) - 10, max(origin_lat, dest_lat) + 10]
    fig.update_layout(
        title=f"{ship_row['Ship Name']} Route: {ship_row['Origin']} → {ship_row['Declared Destination']}",
        geo=dict(
            projection_type='natural earth',
            showland=True,
            showcountries=True,
            landcolor='rgb(230, 230, 230)',
            lonaxis=dict(range=lon_range),  # Adjust the longitude range dynamically
            lataxis=dict(range=lat_range),  # Adjust the latitude range dynamically
            center=dict(lon=(origin_lon + dest_lon) / 2, lat=(origin_lat + dest_lat) / 2),  # Center map between origin and destination
            projection_scale=6,              # Adjust projection scale for proper view
            scrollzoom=False,                # Disable scroll zoom
        ),
        height=1200,
        width=1500
    )

    return fig
if __name__ == '__main__':
    app.run(debug=True)

'''

"""
 fig.update_layout(
        title=f"{ship_row['Ship Name']} Route: {ship_row['Origin']} → {ship_row['Declared Destination']}",
        geo=dict(
            projection_type='natural earth',
            showland=True,
            showcountries=True,
            landcolor='rgb(230, 230, 230)'
        ),
        height=1200,
        width=1500
    )

    return fig
"""

import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from geopy.geocoders import Nominatim

testing = pd.DataFrame({
    'Ship Name': ['Dispatch', 'Rufus', 'Polly', 'Ocean', 'Hannah', 'Two Brothers', 'Susan', 'Patty', 'Polly', 'THE_RONZOR'],
    'Origin': ['Savannah', 'Savannah', 'Petersburg', 'Isle of France', 'Boston', 'Boston', 'Málaga, Spain', 'Norfolk', 'Cape Francoise', 'London'],
    'Declared Destination': ['Boston', 'Liverpool', 'Boston', 'Boston', 'St. Croix', 'Falmouth', 'Rouen', 'Marseilles', 'New York', 'Savannah']
})


geolocator = Nominatim(user_agent="ship-route-demo")


def get_coordinates(city_name):
    try:
        location = geolocator.geocode(city_name)
        return (location.latitude, location.longitude) if location else (None, None)
    except:
        return (None, None)

def create_route_with_midpoint(origin, dest):
    origin_lat, origin_lon = origin
    dest_lat, dest_lon = dest

    # Rough check: if one point is in Europe/Africa and the other in the Americas
    if (origin_lon < -30 and dest_lon > -30) or (origin_lon > -30 and dest_lon < -30):
        mid_lat = (origin_lat + dest_lat) / 2
        mid_lon = -30  # Mid-Atlantic
        return [origin_lon, mid_lon, dest_lon], [origin_lat, mid_lat, dest_lat]
    else:
        return [origin_lon, dest_lon], [origin_lat, dest_lat]
    

testing['Origin Lat'], testing['Origin Lon'] = zip(*testing['Origin'].map(get_coordinates))
testing['Dest Lat'], testing['Dest Lon'] = zip(*testing['Declared Destination'].map(get_coordinates))


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Ship Route Visualizer", style={'textAlign': 'center'}),

    html.Label("Select Ship:"),
    dcc.Dropdown(
        id='ship-dropdown',
        options=[{'label': name, 'value': name} for name in testing['Ship Name']],
        value='Dispatch'  # Default value updated to a valid ship name
    ),

    dcc.Graph(
    id='route-map',
    style={'marginTop': 10},
    config={
        'scrollZoom': False,  # This disables zoom with mouse scroll
        'staticPlot': True,  # Set to True to disable all interactivity (optional)
    }
)
])

@app.callback(
    Output('route-map', 'figure'),
    Input('ship-dropdown', 'value')
)
def update_map(ship_name):
    # Get the row corresponding to the selected ship
    ship_row = testing[testing['Ship Name'] == ship_name].iloc[0]
    
    # Check if coordinates are valid for both origin and destination
    origin_lat, origin_lon = ship_row['Origin Lat'], ship_row['Origin Lon']
    dest_lat, dest_lon = ship_row['Dest Lat'], ship_row['Dest Lon']
    
    if None in [origin_lat, origin_lon, dest_lat, dest_lon]:
        # If any of the coordinates are invalid, return an empty figure or error message
        return {
            'data': [],
            'layout': go.Layout(
                title=f"Error: Invalid Coordinates for {ship_name}",
                geo=dict(
                    projection_type='natural earth',
                    showland=True,
                    showcountries=True,
                    landcolor='rgb(230, 230, 230)'
                ),
                height=1200,
                width=1500
            )
        }

    fig = go.Figure()

    lons, lats = create_route_with_midpoint((origin_lat, origin_lon), (dest_lat, dest_lon))

    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='lines+markers',
        line=dict(width=2, color='blue'),
        marker=dict(size=6, color='blue'),
        name=f"{ship_row['Ship Name']} Route"
    ))

    # Add arrowhead using a triangle-up marker at the destination
    fig.add_trace(go.Scattergeo(
        lon=[dest_lon],
        lat=[dest_lat],
        mode='markers',
        marker=dict(
            size=12,
            symbol='triangle-up',
            color='blue',
            angle=0  # Note: angle is not supported in scattergeo, so arrowhead will always point up
        ),
        name='Destination (Arrowhead)'
    ))


    # Apply to figure
    fig.update_layout(
        title=f"{ship_row['Ship Name']} Route: {ship_row['Origin']} → {ship_row['Declared Destination']}",
        geo=dict(
            projection_type='natural earth',
            showland=True,
            showcountries=True,
            landcolor='rgb(230, 230, 230)'
        ),
        height=1200,
        width=1500
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
