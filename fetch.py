import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import requests
from base64 import b64encode

# Fetch data from the provided OData link
url = "http://bc.deepcatchgroup.com:7823/DT_BC21_DCT_UP/ODataV4/Company('Seapride%20-%20Food%20Services%20LIVE')/items"
headers = {
    "Content-Type": "application/json",
    "Authorization": "Basic " + b64encode(b"Lothart:Deepcatch@2023").decode('utf-8')
}
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Print the full JSON response for inspection
    print(response.json())
    # Extract the 'value' key from the JSON response
    data = response.json().get("value", [])
    df = pd.DataFrame(data)
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")

# ... rest of your code ...
