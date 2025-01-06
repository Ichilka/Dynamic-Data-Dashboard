# Import required libraries
from dash import Dash, dcc, html, Input, Output, State, dash_table
import pandas as pd
import plotly.express as px
import io
import base64

# Create Dash app & Define layout
app = Dash(__name__)
app.title = "Dynamic CSV Dashboard"

app.layout = html.Div([
    html.H1("Dynamic CSV Dashboard", style={'textAlign': 'center'}),
    
    # File upload section
    html.Div([
        dcc.Upload(
            id = 'upload-data',
            children = html.Div(['Drag and Drop or ', html.A('Select a CSV File')]),
            style = {
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple = False  # Only one file at a time
        ),
    ]),
    
    # Display uploaded data table
    html.Div(id = 'data-table-container'),
    
    # Graphs
    html.Div([
        dcc.Graph(id = 'graph-1'),
        dcc.Graph(id = 'graph-2'),
        dcc.Graph(id = 'graph-3'),
    ])
])

# Function to parse uploaded file
def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string).decode('utf-8')
    return pd.read_csv(io.StringIO(decoded))

# Callback for processing uploaded data
@app.callback(
    [Output('data-table-container', 'children'),
     Output('graph-1', 'figure'),
     Output('graph-2', 'figure'),
     Output('graph-3', 'figure')],
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename')]
)
def update_dashboard(contents, filename):
    if contents is None:
        return html.Div("No data uploaded yet."), {}, {}, {}
    
    # Parse uploaded file
    try:
        data = parse_contents(contents)
    except Exception as e:
        return html.Div(f"Error processing {filename}: {str(e)}"), {}, {}, {}
    
    # Display table
    table = dash_table.DataTable(
        data=data.head().to_dict('records'),
        columns=[{"name": i, "id": i} for i in data.columns],
        style_table={'overflowX': 'auto'}
    )
    
    # Generate graphs dynamically based on columns
    if len(data.columns) >= 2:
        fig1 = px.bar(data, x=data.columns[0], y=data.columns[1], title=f"{data.columns[1]} by {data.columns[0]}")
    else:
        fig1 = {}

    if len(data.columns) >= 3:
        fig2 = px.line(data, x=data.columns[0], y=data.columns[2], title=f"{data.columns[2]} over {data.columns[0]}")
    else:
        fig2 = {}

    if len(data.columns) >= 4:
        fig3 = px.pie(data, names=data.columns[3], title=f"Distribution of {data.columns[3]}")
    else:
        fig3 = {}

    return table, fig1, fig2, fig3

# Run the app
if __name__ == '__main__':
    app.run_server(debug = True)