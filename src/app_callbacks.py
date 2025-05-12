import pandas as pd
import plotly.graph_objects as go
from dash import html
from typing import Tuple, List
from src.Port_Waypoints import port_waypoints

LONGITUDE_CUTOFF: float = -30.0

def get_routed_path(ship_row: pd.Series) -> Tuple[List[float], List[float]]:
    origin_name: str = ship_row['Origin']
    destination_name: str = ship_row['Declared Destination']

    origin: Tuple[float, float] = (ship_row['Origin Lat'], ship_row['Origin Lon'])
    destination: Tuple[float, float] = (ship_row['Dest Lat'], ship_row['Dest Lon'])

    route: List[Tuple[float, float]] = [origin]

    if origin_name in port_waypoints:
        route.extend(port_waypoints[origin_name])

    if origin[1] > LONGITUDE_CUTOFF and destination[1] < LONGITUDE_CUTOFF:
        route.extend([
            port_waypoints['Canary Islands'][0],
            port_waypoints['Caribbean'][0]
        ])

    if destination_name in port_waypoints:
        route.extend(reversed(port_waypoints[destination_name]))

    route.append(destination)
    return list(zip(*route))  # Returns (lats, lons)


def update_map(ship_name: str, ship_data: pd.DataFrame) -> go.Figure:
    ship_row: pd.Series = ship_data[ship_data['Ship Name'] == ship_name].iloc[0]
    origin_lat: float = ship_row['Origin Lat']
    origin_lon: float = ship_row['Origin Lon']
    dest_lat: float = ship_row['Dest Lat']
    dest_lon: float = ship_row['Dest Lon']

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

    fig.add_trace(go.Scattergeo(
        lon=lons,
        lat=lats,
        mode='lines+markers',
        line=dict(width=2, color='blue'),
        marker=dict(size=6, color='blue'),
        name=f"{ship_row['Ship Name']} Route"
    ))

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
    ship_row: pd.Series = ship_data[ship_data['Ship Name'] == ship_name].iloc[0]
    return html.Div([
        html.H4(f"{ship_name} Information"),
        html.P(f"Year: {ship_row['Year']}"),
        html.P(f"Captain: {ship_row['Captain']}"),
        html.P(f"Cargo: {ship_row['Cargo']}")
    ])
