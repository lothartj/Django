import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import requests
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta

# Replace this URL with your actual OData endpoint
odata_url = "http://bc.deepcatchgroup.com:7803/DT_BC21_RET_UP/ODataV4/Company('Seapride%20Foods%20Retail')/React_Services_PostedSalesOrders"

# Replace with your actual credentials
username = "Lothart"
password = "Deepcatch@2023"

# Basic authentication for OData
auth = (username, password)

# Fetch data from OData and convert it to a DataFrame
response = requests.get(odata_url, auth=auth)
data = response.json()['value']
df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# Define layout
app.layout = html.Div([
    html.H1("Sales Dashboard"),
    
    # Create a dropdown for selecting the analysis point
    dcc.Dropdown(
        id='analysis-dropdown',
        options=[
            {'label': 'Analyzing sales trends over time', 'value': 'sales_trends'},
            {'label': 'Monitoring customer buying behavior', 'value': 'customer_behavior'},
            {'label': 'Managing inventory and shipment logistics', 'value': 'inventory_logistics'},
            {'label': 'Assessing financial performance', 'value': 'financial_performance'},
        ],
        value='sales_trends'
    ),

    # Display the selected analysis point
    html.Div(id='selected-analysis'),

    # Graph for visualization
    dcc.Graph(id='analysis-graph'),

    dcc.Interval(
        id='interval-component',
        interval=30*1000,  # in milliseconds
        n_intervals=0
    )
])

# Callback to update the graph based on the selected analysis point
@app.callback(
    [Output('selected-analysis', 'children'),
     Output('analysis-graph', 'figure')],
    [Input('analysis-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graph(selected_analysis, n_intervals):
    # Fetch data again to get the latest data
    response = requests.get(odata_url, auth=auth)
    data = response.json()['value']
    df = pd.DataFrame(data)

    # Process data based on the selected analysis point
    if selected_analysis == 'sales_trends':
        # Process data for sales trends analysis
        # Example: Group by date and sum the amount
        processed_data = df.groupby('Posting_Date')['Amount'].sum().reset_index()
        x_values = processed_data['Posting_Date']
        y_values = processed_data['Amount']

        graph_title = 'Sales Trends Over Time'
        x_axis_label = 'Date'
        y_axis_label = 'Total Sales Amount'

    elif selected_analysis == 'customer_behavior':
        # Process data for customer behavior analysis
        # Example: Group by customer and count orders
        processed_data = df.groupby('Sell_to_Customer_Name')['No'].count().reset_index()
        x_values = processed_data['Sell_to_Customer_Name']
        y_values = processed_data['No']

        graph_title = 'Customer Buying Behavior'
        x_axis_label = 'Customer Name'
        y_axis_label = 'Number of Orders'

    elif selected_analysis == 'inventory_logistics':
        # Process data for inventory and logistics analysis
        # Example: Group by location and count orders
        processed_data = df.groupby('Location_Code')['No'].count().reset_index()
        x_values = processed_data['Location_Code']
        y_values = processed_data['No']

        graph_title = 'Inventory and Shipment Logistics'
        x_axis_label = 'Location Code'
        y_axis_label = 'Number of Orders'

    elif selected_analysis == 'financial_performance':
        # Process data for financial performance analysis
        # Example: Group by date and sum the amount including VAT
        processed_data = df.groupby('Posting_Date')['Amount_Including_VAT'].sum().reset_index()
        x_values = processed_data['Posting_Date']
        y_values = processed_data['Amount_Including_VAT']

        graph_title = 'Financial Performance Over Time'
        x_axis_label = 'Date'
        y_axis_label = 'Total Amount Including VAT'

    else:
        x_values = []
        y_values = []
        graph_title = 'No Data'
        x_axis_label = ''
        y_axis_label = ''

    # Update the graph layout
    figure = {
        'data': [
            {'x': x_values, 'y': y_values, 'type': 'bar', 'name': selected_analysis},
        ],
        'layout': {
            'title': graph_title,
            'xaxis': {'title': x_axis_label},
            'yaxis': {'title': y_axis_label},
        }
    }

    return f"Selected Analysis: {selected_analysis}", figure

if __name__ == '__main__':
    app.run_server(debug=True)
