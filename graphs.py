import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Dash
from dash import html, dcc
from dash.dependencies import Input, Output

# Load your cleaned and combined dataset
df = pd.read_csv('CombinedDoc_new.csv')

# Create a Dash web application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

graph_controls = dbc.Card([
    dbc.Row([
        dbc.Label('Country', html_for="country_choice"),
        dcc.Dropdown(
            id='country_choice',
            options=[{'label': cn, 'value': cn} for cn in sorted(df['Country'].unique())],
            value=sorted(df['Country'].unique())[0],
            multi=True  # Allow multiple selections
        ),
        dbc.Label('Local Authority', html_for="local-authority"),
        dcc.Dropdown(
            id='local-authority',
            options=[],  # Options will be dynamically populated based on the selected country
            value=[sorted(df[df['Country'] == sorted(df['Country'].unique())[0]]['Local_Authority'].unique())[0]],
            multi=True  # Allow multiple selections
        ),
    ]),
], body=True)


@app.callback(
    Output('local-authority', 'options'),
    Input('country_choice', 'value')
)
def update_local_authorities(selected_countries):
    # Convert the input to a list if it's a string
    if isinstance(selected_countries, str):
        selected_countries = [selected_countries]
    # Handle case when no country is selected
    if not selected_countries:
        return []

    # Filter the DataFrame based on selected countries
    filtered_df = df[df['Country'].isin(selected_countries)]

    # Get unique local authorities from the filtered DataFrame
    local_authorities = sorted(filtered_df['Local_Authority'].unique())

    # Create options for the Local Authority dropdown
    options = [{'label': la, 'value': la} for la in local_authorities]

    return options


app.layout = dbc.Container(
    [
        html.H1("Household Carbon Emission vs Income"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(graph_controls, width=2),
                dbc.Col([
                    html.Div([dcc.Graph(id='income-vs-years-plot')], style={'display': 'inline-block', 'width': '50%'}),
                    html.Div([dcc.Graph(id='total-usage-vs-years-plot')],
                             style={'display': 'inline-block', 'width': '50%'}),
                    html.Div([dcc.Graph(id='gas-usage-vs-years-plot')],
                             style={'display': 'inline-block', 'width': '50%'}),
                    html.Div([dcc.Graph(id='electricity-usage-vs-years-plot')],
                             style={'display': 'inline-block', 'width': '50%'}),
                    html.Div([dcc.Graph(id='other-usage-vs-years-plot')],
                             style={'display': 'inline-block', 'width': '50%'}),

                ], width=10),

            ],
        ),

    ],
    fluid=True,
)


@app.callback(
    [
        Output('income-vs-years-plot', 'figure'),
        Output('gas-usage-vs-years-plot', 'figure'),
        Output('electricity-usage-vs-years-plot', 'figure'),
        Output('other-usage-vs-years-plot', 'figure'),
        Output('total-usage-vs-years-plot', 'figure')],
    Input('local-authority', 'value')

)
def update_plots(selected_local_authorities):
    filtered_data = df[df['Local_Authority'].isin(selected_local_authorities)]
    income_vs_years_plot = px.line(filtered_data, x='Year', y='Income_Per_Capita', color='Local_Authority')
    gas_usage_vs_years_plot = px.line(filtered_data, x='Year', y='Gas_Per_Capita', color='Local_Authority')
    electricity_usage_vs_years_plot = px.line(filtered_data, x='Year', y='Electricity_Per_Capita',
                                              color='Local_Authority')
    other_usage_vs_years_plot = px.line(filtered_data, x='Year', y='Other_Per_Capita', color='Local_Authority')
    total_usage_vs_years_plot = px.line(filtered_data, x='Year', y='Total_Per_Capita', color='Local_Authority')

    income_vs_years_plot.update_layout(
        yaxis_title='Per Capita Income'
    )
    gas_usage_vs_years_plot.update_layout(
        yaxis_title='Per Capita Gas Emission(CO2)'
    )
    electricity_usage_vs_years_plot.update_layout(
        yaxis_title='Per Capita Electricity Emission(CO2)'
    )
    other_usage_vs_years_plot.update_layout(
        yaxis_title='Per Capita Emission- Others(CO2)'
    )
    total_usage_vs_years_plot.update_layout(
        yaxis_title='Per Capita Total Emission(CO2)'
    )

    return income_vs_years_plot, gas_usage_vs_years_plot, electricity_usage_vs_years_plot, other_usage_vs_years_plot, total_usage_vs_years_plot


# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
    # app.run_server(debug=False, host = "0.0.0.0", port = 8080)
