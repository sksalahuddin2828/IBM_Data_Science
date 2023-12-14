# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv', 
                            encoding = "ISO-8859-1",
                            dtype={'Div1Airport': str, 'Div1TailNum': str, 
                                   'Div2Airport': str, 'Div2TailNum': str})

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                
                                  dcc.Dropdown(id='site-dropdown',
                                    options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                                            ],
                                    value='ALL',
                                    placeholder="Select a Launch Site here",
                                    searchable=True
                                 ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                    min=0, max=10000, step=1000,
                                    marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000', 6000: '6000', 
                                    7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'}, 
                                    value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Ad# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
              
def get_pie_chart(entered_site):
    filtered_df = spacex_df[spacex_df['class'] == 1]
    if entered_site == 'ALL':
        fig = px.pie(filtered_df,
        values = 'class',
        names='Launch Site', 
        title='Total Success Launces By All Sites')
        return fig
    else:
        specific_site = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie (specific_site,
        names = 'class',
        title = 'Launch status by: ' + entered_site)
        return fig
        # return the outcomes piechart for a selected site

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'),
              Input(component_id="payload-slider", component_property="value"))

def get_scatter_slider_chart(entered_site, payload_slider):
    lowPayload, highPayload = payload_slider
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] > lowPayload) & (spacex_df['Payload Mass (kg)'] < highPayload)]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df, 
        x = 'Payload Mass (kg)',
        y = 'class',
        color = 'Booster Version Category',
        title = 'Correlation Between Payload and Mission Outcomes For All Sites')
        return fig
    else:
        fig = px.scatter(filtered_df[filtered_df['Launch Site'] == entered_site],
        x = 'Payload Mass (kg)',
        y = 'class',
        color = 'Booster Version Category',
        title = 'Correlation Between Payload And Mission Outcomes for: ' + entered_site)
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
