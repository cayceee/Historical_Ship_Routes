import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go

# Load data
shipData = pd.read_csv("New_England_Processed.csv")[["Ship_Name", "Origin", "DestinationDecl"]].rename(
    columns={
        "Ship_Name": "Ship Name",
        "DestinationDecl": "Declared Destination"
    }
)

coords = pd.read_csv("geocoded_locations_clean.csv")

# Merge origin and destination coordinates
shipData = shipData.merge(
    coords.rename(columns={"Location": "Origin", "Latitude": "Origin Lat", "Longitude": "Origin Lon"}),
    on="Origin", how="left"
)
shipData = shipData.merge(
    coords.rename(columns={"Location": "Declared Destination", "Latitude": "Dest Lat", "Longitude": "Dest Lon"}),
    on="Declared Destination", how="left"
)

# Define port_waypoints as in your code (not shown here to save space)
# Routing waypoints for more realistic sea routes
port_waypoints = {
    'London': [
        (51.5, 0.0),        # Port of London
        (51.0, -1.5),       # English Channel Entrance
        (49.0, -6.0),       # Channel Exit to Atlantic
        (48.0, -10.0),      # Heading toward Atlantic (north of Ireland)
    ],
    'Liverpool': [
        (53.4, -3.0),       # Mersey River mouth
        (51.5, -8.0),       # Heading west from Liverpool (to Irish Sea)
        (50.0, -6.0),       # Heading out into the Atlantic (west of Ireland)
    ],
    'Boston': [
        (42.3, -70.8),      # Boston Harbor
        (41.0, -70.0),      # Out to the Atlantic
        (40.0, -72.0),      # Continuing out of Boston's proximity
        (39.0, -74.0),      # Heading east towards Europe
    ],
    'Norfolk': [
        (36.9, -76.2),      # Chesapeake Bay
        (36.5, -74.0),      # Atlantic Ocean exit (toward Europe)
        (37.0, -75.0),      # Heading south toward Europe/Caribbean
    ],
    'Savannah': [
        (32.1, -81.1),      # Savannah River
        (30.0, -76.0),      # Heading out to the Atlantic
        (31.0, -77.0),      # Heading toward the Caribbean
    ],
    'New York': [
        (40.7, -74.0),      # Port of New York
        (40.0, -72.0),      # Heading out into the Atlantic
        (39.0, -71.0),      # Heading eastward toward Europe
    ],
    'Rouen': [
        (49.4, 0.1),        # Port of Rouen (Seine river mouth)
        (49.3, 0.3),        # Heading into English Channel
        (50.0, 1.5),        # Exiting toward the North Sea/Atlantic
    ],
    'Cape Francoise': [
        (19.8, -72.0),      # Bay mouth (origin)
        (20.0, -72.5),      # Heading toward Caribbean
        (21.0, -73.0),      # Heading further toward South America
    ],
    'Marseilles': [
        (43.3, 5.3),        # Port of Marseilles
        (42.5, 6.0),        # Heading into Mediterranean
        (36.0, -5.5),       # Exiting via Gibraltar Strait
    ],
    'Falmouth': [
        (50.1, -5.0),       # Port of Falmouth
        (48.0, -8.0),       # Heading out into the Atlantic
        (47.5, -9.0),       # Heading towards the Bay of Biscay
    ],
    'Petersburg': [
        (37.2, -77.3),      # Port of Petersburg (James River)
        (36.9, -76.2),      # Heading into Chesapeake Bay
        (36.0, -77.5),      # Heading into Atlantic
    ],
    'Isle of France': [
        (-20.2, 57.5),      # Mauritius (Port Louis)
        (-33.9, 18.4),      # Cape of Good Hope (around Africa)
        (-28.0, 16.0),      # Southern Africa coast (heading toward Atlantic)

    ],
    'Gibraltar': [
        (36.1, -5.3),       # Port of Gibraltar
        (36.0, -5.5),       # Exiting into the Atlantic
        (37.0, -5.5),       # Heading westward (destination)
    ],
}

port_waypoints.update({
    'Martinico': [(15.0, -60.5)],  # Caribbean approach
    'Demerara': [(6.8, -58.2)],  # Near modern Georgetown, Guyana
    'Philadelphia': [(39.5, -74.5)],
    'Alexandria': [(32.0, 24.0), (10.0, 40.0), (-20.0, 50.0)],  # Around Africa
    'Antigua': [(17.1, -61.9)],
    'Amsterdam': [(53.0, 4.0), (51.0, -2.0)],  # English Channel entry
    'Portsmouth': [(50.7, -1.3), (51.0, -2.0)],  # Solent to Channel
    'Barbadoes': [(13.0, -59.6)],
    'Salem': [(42.5, -69.5)],
    'Portland': [(43.5, -69.0)],
    'Lisbon': [(38.7, -9.2), (37.0, -13.0)],  # To Atlantic route
    'Bourdeaux': [(45.0, -1.0), (43.0, -10.0)],  # Into Atlantic
    'Madeira': [(32.7, -16.9)],
    'St. Croix': [(17.7, -64.8)],
    'Trinadad': [(10.6, -61.5)],
    'Richmond': [(37.0, -76.0)],
    'Greenock': [(55.9, -4.7), (51.0, -10.0)],  # Scotland via Atlantic
    'Cadiz': [(36.5, -6.3), (35.5, -9.0)],  # Gibraltar Strait
    'Jamaica': [(18.0, -76.8)],
    'St. Johns': [(47.6, -52.7)],
    'Havana': [(23.0, -82.5)],
    'West-Indies': [(15.0, -60.0)],  # General Caribbean waypoint
    'Baltimore': [(39.0, -74.0)],
    'Charleston': [(32.5, -78.0)],
    'New Bedford': [(41.4, -70.8)],
    'St. Thomas': [(18.3, -64.9)],
    'Wilmington': [(34.0, -77.0)],
    'Tobago': [(11.3, -60.7)],
    'Rotterdam': [(52.0, 4.5), (51.0, -2.0)],
    'Halifax': [(44.6, -63.6)],
    'Guadaloupe': [(16.2, -61.5)],
    'New Orleans': [(29.0, -89.5)],
    'Windsor': [(44.9, -63.0)],
    'Plymouth': [(50.4, -4.1), (51.0, -2.0)],
    'Yarmouth': [(43.8, -66.1)],
    'Trinidad': [(10.6, -61.5)],
    'New Haven': [(41.2, -72.5)],
    'New London': [(41.3, -72.0)],
    'Gloucester': [(42.6, -70.6)],
    'Newbern': [(35.1, -77.0)],
    'Martinique': [(14.6, -61.1)],
})

# Routing function
def get_routed_path(ship_row):
    origin_name = ship_row['Origin']
    dest_name = ship_row['Declared Destination']

    origin = (ship_row['Origin Lat'], ship_row['Origin Lon'])
    dest = (ship_row['Dest Lat'], ship_row['Dest Lon'])

    route = [origin]
    if origin_name in port_waypoints:
        route.extend(port_waypoints[origin_name])
    if dest_name in port_waypoints:
        route.extend(reversed(port_waypoints[dest_name]))
    route.append(dest)
    return list(zip(*route))

# Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Ship Route Visualizer", style={'textAlign': 'center'}),

    html.Div([
        html.Label("Select Origin Port:"),
        dcc.Dropdown(
            id='origin-port',
            options=[{'label': port, 'value': port} for port in sorted(shipData['Origin'].dropna().unique())],
            value=None
        ),
    ], style={'marginBottom': 10}),

    html.Div([
        html.Label("Select Destination Port:"),
        dcc.Dropdown(
            id='destination-port',
            options=[{'label': port, 'value': port} for port in sorted(shipData['Declared Destination'].dropna().unique())],
            value=None
        ),
    ], style={'marginBottom': 10}),

    html.Div([
        html.Label("Select Ship:"),
        dcc.Dropdown(id='ship-dropdown'),
    ], style={'marginBottom': 20}),

    dcc.Graph(id='route-map', style={'marginTop': 10}, config={'scrollZoom': False, 'staticPlot': True})
])

@app.callback(
    Output('ship-dropdown', 'options'),
    Output('ship-dropdown', 'value'),
    Input('origin-port', 'value'),
    Input('destination-port', 'value')
)
def update_ships(origin, destination):
    filtered = shipData[(shipData['Origin'] == origin) & (shipData['Declared Destination'] == destination)]
    options = [{'label': name, 'value': name} for name in filtered['Ship Name'].unique()]
    value = options[0]['value'] if options else None
    return options, value

@app.callback(
    Output('route-map', 'figure'),
    Input('ship-dropdown', 'value'),
    Input('origin-port', 'value'),
    Input('destination-port', 'value')
)
def update_map(ship_name, origin, destination):
    filtered = shipData[(shipData['Ship Name'] == ship_name) &
                        (shipData['Origin'] == origin) &
                        (shipData['Declared Destination'] == destination)]

    if filtered.empty:
        return go.Figure(layout=go.Layout(
            title=f"No Data for Ship: {ship_name}",
            geo=dict(projection_type='natural earth', showland=True, showcountries=True, landcolor='rgb(230, 230, 230)'),
            height=1200, width=1500
        ))

    ship_row = filtered.iloc[0]

    lats, lons = get_routed_path(ship_row)

    fig = go.Figure()
    fig.add_trace(go.Scattergeo(
        lon=lons, lat=lats,
        mode='lines+markers',
        line=dict(width=2, color='blue'),
        marker=dict(size=6, color='blue'),
        name=f"{ship_row['Ship Name']} Route"
    ))
    fig.add_trace(go.Scattergeo(
        lon=[lons[-1]], lat=[lats[-1]],
        mode='markers',
        marker=dict(size=12, symbol='triangle-up', color='blue'),
        name='Destination (Arrowhead)'
    ))

    fig.update_layout(
        title=f"{ship_row['Ship Name']} Route: {ship_row['Origin']} → {ship_row['Declared Destination']}",
        geo=dict(projection_type='natural earth', showland=True, showcountries=True, landcolor='rgb(230, 230, 230)'),
        height=1200, width=1500
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
