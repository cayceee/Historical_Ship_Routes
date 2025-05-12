import pandas as pd
import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
from src.app_callbacks import update_map, display_ship_info

ship_data = pd.read_csv("England_New_Data.csv")

# Dash app layout
app = dash.Dash(__name__)

app.layout = html.Div([
    html.Img(
        src='/assets/ship_logo.png',
        style={
            'display': 'block',
            'margin': '0 auto',
            'height': '300px',
            'marginBottom': '5px'
        }
    ),

    html.Label("Select Ship:", style={'marginTop': 5, 'marginBottom': 2}),

    dcc.Dropdown(
        id='ship-dropdown',
        options=[{'label': name, 'value': name} for name in ship_data['Ship Name'].unique()],
        value=ship_data['Ship Name'].iloc[0],
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
    style={'backgroundColor': '#6495ED', 'padding': '10px'}
)


@app.callback(
    Output('route-map', 'figure'),
    Input('ship-dropdown', 'value')
)
def handle_update_map(ship_name: str) -> go.Figure:
    return update_map(ship_name, ship_data)


@app.callback(
    Output('ship-info', 'children'),
    Input('ship-dropdown', 'value')
)
def handle_display_ship_info(ship_name: str) -> html.Div:
    return display_ship_info(ship_name, ship_data)


if __name__ == '__main__':
    app.run(debug=True)
