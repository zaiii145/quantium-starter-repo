import pandas as pd
import dash
from dash import dcc
from dash import html
import plotly.express as px
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate

# -----------------------------------------------------------------------------
# 1. Load and Prepare Data
# -----------------------------------------------------------------------------

# This script assumes 'processed_data.csv' exists in the same directory.
# This file was generated in the previous step of the project.
try:
    df = pd.read_csv('processed_data.csv')
    df['date'] = pd.to_datetime(df['date'])  # Ensure 'date' column is in datetime format
except FileNotFoundError:
    print("Error: The 'processed_data.csv' file was not found.")
    print("Please ensure you have completed the previous task and the file is in the correct directory.")
    # Exit the script gracefully if the data file is missing
    raise PreventUpdate

# Sort the DataFrame by date to ensure the line chart is drawn correctly.
df = df.sort_values(by='date')

# -----------------------------------------------------------------------------
# 2. Create the Dash Application
# -----------------------------------------------------------------------------

app = dash.Dash(__name__)

# -----------------------------------------------------------------------------
# 3. Design the Dashboard Layout
# -----------------------------------------------------------------------------

# Create the main line chart using Plotly Express.
# The color parameter is used to show a separate line for each region.
fig = px.line(
    df,
    x="date",
    y="Sales",
    color="region",
    title="Pink Morsel Sales Over Time",
    labels={
        "date": "Date",
        "Sales": "Total Sales ($)",
        "region": "Region"
    }
)

# Add a vertical line to mark the date of the price increase.
# The x-coordinate is passed as a string.
fig.add_vline(
    x='2021-01-15',
    line_width=2,
    line_dash="dash",
    line_color="red"
)

# Customize the layout for better readability.
fig.update_layout(
    plot_bgcolor='#f9f9f9',  # Light gray background for the plot area
    paper_bgcolor='#ffffff',  # White background for the entire figure
    font_family="Arial",
    font_color="#333",
    title_font_size=24,
    title_x=0.5,  # Center the title
    hovermode="x unified"  # Show sales for all regions on the same date when hovering
)

app.layout = html.Div(style={'font-family': 'Arial, sans-serif', 'padding': '20px'}, children=[
    # Header of the dashboard
    html.H1(
        children='Soul Foods - Pink Morsel Sales Performance',
        style={
            'textAlign': 'center',
            'color': '#333',
            'margin-bottom': '20px'
        }
    ),

    # A brief introduction for context
    html.Div(
        children='This dashboard visualizes the daily sales of Pink Morsels. The red dashed line indicates the date of the price increase on January 15th, 2021.',
        style={
            'textAlign': 'center',
            'color': '#666',
            'margin-bottom': '30px'
        }
    ),

    # The main graph component
    dcc.Graph(
        id='sales-line-chart',
        figure=fig
    )
])

# -----------------------------------------------------------------------------
# 4. Run the Application
# -----------------------------------------------------------------------------

# To run the app, execute this script from your terminal.
# Open a web browser and navigate to http://127.0.0.1:8050/
if __name__ == '__main__':
    app.run(debug=True)