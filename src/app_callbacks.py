import pandas as pd
import plotly.graph_objects as go
from dash import html
from typing import Tuple, List
from src.Port_Waypoints import port_waypoints

#For Determining ships traveling east to west across the Atlantic
LONGITUDE_CUTOFF: float = -30.0

def get_routed_path(ship_row: pd.Series) -> Tuple[List[float], List[float]]:
    """
    Computes the full routed path (latitude and longitude lists) for a ship row.
    Adds waypoints if applicable and includes transatlantic adjustments based on a longitude cutoff.
    """
    origin_name: str = ship_row['Origin']
    destination_name: str = ship_row['Declared Destination']

    origin: Tuple[float, float] = (ship_row['Origin Lat'], ship_row['Origin Lon'])
    destination: Tuple[float, float] = (ship_row['Dest Lat'], ship_row['Dest Lon'])

    route: List[Tuple[float, float]] = [origin]

    # Add origin-specific waypoints
    if origin_name in port_waypoints:
        route.extend(port_waypoints[origin_name])

    # Add Canary Islands and Caribbean waypoints if crossing the Atlantic westward
    if origin[1] > LONGITUDE_CUTOFF and destination[1] < LONGITUDE_CUTOFF:
        route.extend([
            port_waypoints['Canary Islands'][0],
            port_waypoints['Caribbean'][0]
        ])

    # Add destination-specific waypoints in reverse order
    if destination_name in port_waypoints:
        route.extend(reversed(port_waypoints[destination_name]))

    route.append(destination)

    return list(zip(*route))  # Returns (latitudes, longitudes)


def update_map(ship_name: str, ship_data: pd.DataFrame) -> go.Figure:
    """
    Generates a Plotly map figure for a selected ship.
    Includes blue route line, green origin marker, and red destination marker.
    """
    ship_row: pd.Series = ship_data[ship_data['Ship Name'] == ship_name].iloc[0]
    origin_lat: float = ship_row['Origin Lat']
    origin_lon: float = ship_row['Origin Lon']
    dest_lat: float = ship_row['Dest Lat']
    dest_lon: float = ship_row['Dest Lon']

    # Handle missing coordinates with an error message
    if pd.isna(origin_lat) or pd.isna(origin_lon) or pd.isna(dest_lat) or pd.isna(dest_lon):
        return go.Figure(
            layout=go.Layout(
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
        )

    lats, lons = get_routed_path(ship_row)

    fig = go.Figure()

    # Plot the route line and waypoints
    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='lines+markers',
        line=dict(width=2, color='blue'),
        marker=dict(size=6, color='blue'),
        name=f"{ship_row['Ship Name']} Route"
    ))

    # Green circle at origin
    fig.add_trace(go.Scattergeo(
        lon=[lons[0]],
        lat=[lats[0]],
        mode='markers',
        marker=dict(
            size=10,
            color='green',
            symbol='circle'
        ),
        name='Origin'
    ))

    # Red triangle at destination
    fig.add_trace(go.Scattergeo(
        lon=[lons[-1]],
        lat=[lats[-1]],
        mode='markers',
        marker=dict(
            size=12,
            symbol='triangle-up',
            color='red'
        ),
        name='Destination'
    ))

    # Map layout settings
    fig.update_layout(
        title=f"{ship_row['Ship Name']} Route: {ship_row['Origin']} → {ship_row['Declared Destination']}",
        geo=dict(
            projection_type='natural earth',
            showland=True,
            showcountries=True,
            landcolor='rgb(230, 230, 230)'
        ),
        height=500,
        width=800
    )

    return fig


def display_ship_info(ship_name: str, ship_data: pd.DataFrame) -> html.Div:
    """
    Creates a formatted HTML div showing metadata for a selected ship.
    Includes year, captain, and cargo.
    """
    ship_row: pd.Series = ship_data[ship_data['Ship Name'] == ship_name].iloc[0]
    return html.Div([
        html.H4(f"{ship_name} Information"),
        html.P(f"Year: {ship_row['Year']}"),
        html.P(f"Captain: {ship_row['Captain']}"),
        html.P(f"Cargo: {ship_row['Cargo']}")
    ])
