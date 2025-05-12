import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from  src.Port_Waypoints import port_waypoints

shipData = pd.read_csv(r"England_New_Data.csv")

def get_routed_path(ship_row):
    origin_name = ship_row['Origin']
    dest_name = ship_row['Declared Destination']

    origin = (ship_row['Origin Lat'], ship_row['Origin Lon'])
    dest = (ship_row['Dest Lat'], ship_row['Dest Lon'])

    route = [origin]

    # Longitude threshold for Europe vs. America
    longitude_cutoff = -30  # Example cutoff for the Atlantic Ocean

    # Add origin waypoints if available
    if origin_name in port_waypoints:
        route.extend(port_waypoints[origin_name])

    # If the ship is traveling from Europe to America, add the Canary Islands and Caribbean waypoints in between
    if origin[1] > longitude_cutoff and dest[1] < longitude_cutoff:
        route.extend([port_waypoints['Canary Islands'][0], port_waypoints['Caribbean'][0]])

    # Add destination waypoints if available
    if dest_name in port_waypoints:
        route.extend(reversed(port_waypoints[dest_name]))

    route.append(dest)
    return list(zip(*route))  # Returns (lats, lons)



# Dash app layout
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Img(src='/assets/ship_logo.png', style={'display': 'block', 'margin': '0 auto', 'height': '300px', 'marginBottom': '5px'}),
    
    html.Label("Select Ship:", style={'marginTop': 5, 'marginBottom': 2}),
    
    dcc.Dropdown(
        id='ship-dropdown',
        options=[{'label': name, 'value': name} for name in shipData['Ship Name'].unique()],
        value=shipData['Ship Name'].iloc[0],
        style={'marginBottom': 5}
    ),
    
    dcc.Graph(
        id='route-map',
        style={'backgroundColor': '#6495ED', 'marginTop': 5, 'marginBottom': 5},
        config={
            'scrollZoom': False,
            'staticPlot': True,
        }
    ),
    
    html.Div(
        id='ship-info',
        style={
            'marginTop': 5,
            'padding': 6,
            'border': '1px solid #ccc',
            'borderRadius': 4,
            'backgroundColor': '#f9f9f9'  
        }
    )
],
style={'backgroundColor': '	#6495ED', 'padding': '10px'}
)



@app.callback(
    Output('route-map', 'figure'),
    Input('ship-dropdown', 'value')
)
def update_map(ship_name):
    ship_row = shipData[shipData['Ship Name'] == ship_name].iloc[0]
    origin_lat, origin_lon = ship_row['Origin Lat'], ship_row['Origin Lon']
    dest_lat, dest_lon = ship_row['Dest Lat'], ship_row['Dest Lon']

    if pd.isna(origin_lat) or pd.isna(origin_lon) or pd.isna(dest_lat) or pd.isna(dest_lon):
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

@app.callback(
    Output('ship-info', 'children'),
    Input('ship-dropdown', 'value')
)
def display_ship_info(ship_name):
    ship_row = shipData[shipData['Ship Name'] == ship_name].iloc[0]
    return html.Div([
        html.H4(f"{ship_name} Information"),
        html.P(f"Year: {ship_row['Year']}"),
        html.P(f"Captain: {ship_row['Captain']}"),
        html.P(f"Cargo: {ship_row['Cargo']}")
    ])

if __name__ == '__main__':
    app.run(debug=True)
