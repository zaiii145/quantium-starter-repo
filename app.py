import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

# -----------------------------------------------------------------------------
# 1. Load and Prepare Data
# -----------------------------------------------------------------------------

# This script assumes 'processed_data.csv' exists in the same directory.
try:
    df = pd.read_csv('processed_data.csv')
    df['date'] = pd.to_datetime(df['date'])
except FileNotFoundError:
    print("Error: The 'processed_data.csv' file was not found.")
    print("Please ensure you have completed the previous task and the file is in the correct directory.")
    raise PreventUpdate

# Sort the DataFrame by date to ensure the line chart is drawn correctly.
df = df.sort_values(by='date')

# -----------------------------------------------------------------------------
# 2. Create the Dash Application with a Title and some styling.
# -----------------------------------------------------------------------------

app = dash.Dash(__name__)

# The Dash layout is defined here, which includes the components and styling.
app.layout = html.Div(style={
    'backgroundColor': '#f0f2f5',
    'font-family': 'Arial, sans-serif',
    'padding': '40px',
    'textAlign': 'center'
}, children=[
    # The main header for the application.
    html.H1(
        children='3D Pink Morsel Sales Analysis',
        style={
            'color': '#333',
            'marginBottom': '20px',
            'fontSize': '40px'
        }
    ),

    # A descriptive subtitle for the dashboard.
    html.Div(
        children='Visualize daily sales of Pink Morsels in 3D, filtered by region.',
        style={
            'color': '#666',
            'marginBottom': '30px',
            'fontSize': '18px'
        }
    ),

    # Radio buttons to filter data by region.
    html.Div(style={'marginBottom': '30px'}, children=[
        dcc.RadioItems(
            id='region-radio',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'North', 'value': 'north'},
                {'label': 'South', 'value': 'south'},
                {'label': 'East', 'value': 'east'},
                {'label': 'West', 'value': 'west'}
            ],
            value='all',  # Default selected value
            labelStyle={'display': 'inline-block', 'marginRight': '20px', 'fontSize': '16px'}
        )
    ]),

    # The main graph component that will be updated by the callback.
    dcc.Graph(
        id='sales-3d-chart',
        style={'height': '800px'}
    )
])


# -----------------------------------------------------------------------------
# 3. Create a callback to update the graph based on user input (radio button).
# -----------------------------------------------------------------------------

@app.callback(
    Output('sales-3d-chart', 'figure'),
    Input('region-radio', 'value')
)
def update_graph(selected_region):
    # Filter the DataFrame based on the selected radio button value.
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]

    # Create the 3D line chart using Plotly Express.
    fig = px.line_3d(
        filtered_df,
        x="date",
        y="Sales",
        z="region",
        color="region",
        title=f"Daily Pink Morsel Sales for {selected_region.title()} Region",
        labels={
            "date": "Date",
            "Sales": "Total Sales ($)",
            "region": "Region"
        }
    )

    # --- FIX for the Callback Error ---
    # The previous fig.add_vline caused an error because it's for 2D plots.
    # This new section adds a vertical line by creating a separate trace.
    price_increase_date = '2021-01-15'
    
    # Get the min and max sales values to determine the height of the vertical line
    max_sales = filtered_df['Sales'].max()
    min_sales = filtered_df['Sales'].min()
    
    # Define a list of regions to add a vertical line for.
    regions_to_draw = filtered_df['region'].unique()
    
    # Add a vertical line for each unique region on the price increase date.
    for region in regions_to_draw:
        fig.add_trace(go.Scatter3d(
            x=[price_increase_date, price_increase_date],
            y=[min_sales, max_sales],
            z=[region, region],
            mode='lines',
            line=dict(color='red', width=4, dash='dash'),
            showlegend=False,
            hoverinfo='text',
            text=f"Price Increase: {price_increase_date}"
        ))

    # Customize the layout for better readability and a clean look.
    fig.update_layout(
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        margin=dict(l=0, r=0, b=0, t=50),
        scene_camera=dict(
            up=dict(x=0, y=0, z=1),
            center=dict(x=0, y=0, z=0),
            eye=dict(x=1.5, y=-1.5, z=1)
        ),
        font=dict(family="Arial", size=12, color="#333"),
        title_font_size=24,
        title_x=0.5
    )

    return fig

# -----------------------------------------------------------------------------
# 4. Run the Application
# -----------------------------------------------------------------------------

# To run the app, execute this script from your terminal.
# Open a web browser and navigate to http://127.0.0.1:8050/
if __name__ == '__main__':
    app.run(debug=True)