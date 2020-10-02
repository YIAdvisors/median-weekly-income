import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
import heroku3
from dash.dependencies import Input, Output

#Ensure dash capabilities are enabled.
#This allows the code to be deployed on an online server.
app = dash.Dash(__name__)
server = app.server

################################################################################
#This code creates a data visualization of the median weekly income for each year.
#The plotly package is used to create the visualization.
#The dash package is used to create an interactive web app.
#################################################################################

# ------------------------------------------------------------------------------
# Import and clean data (importing csv into pandas)
df = pd.read_csv("median_weekly_income.csv")
#print(df[:5])

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    #Create title
    html.H1("Median Weekly Income by Age", style={'text-align': 'center', 'color':'#2c3e65', 'fontFamily':'Arial, serif'}),

    #Creates a Plotly choropleth map graph.
    dcc.Graph(id='medianIncomeGraph', figure={},config={
                'displayModeBar': False}),

    #Create a link to the data source.
    dcc.Link(
        href='https://cps.ipums.org/cps/',
        refresh=True,
        children=[html.Div(children='Source: Current Population Survey', style={'text-align': 'right','margin-right': '5%', 'color':'#3c90ce', 'fontFamily':'Arial, serif'})]
    ),

    #Display the option from the slider the user has selected. (It is currently disabeled. to enable, change the code in the app.callback so that container = "option_slctd")
    html.Div(id='output_container', children=[])


])


#------------------------------------------------------------------------------
# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='medianIncomeGraph', component_property='figure')],
     [Input(component_id='medianIncomeGraph', component_property='config')] #This is a sneaky way of using the dynamic updating of dash without passing user selected information like in the other apps.
    #[Input(component_id='slct_year', component_property='value')]
)

def update_graph(option_slctd):
    #Code to dynamically display the selected option is in the comment below:
    #container = "selected year: {}".format(option_slctd)
    container = ""

    #Create a new dataframe that is formatted appropriately for a barchart
    dff = pd.DataFrame(
        {'Median Income': df['Median Weekly Earnings'],
         'Year': df['Year'],
         'Group': df['Group']
        })

    #Create separate dataframes for each age group.
    dffAdults = dff[dff["Group"] == "Adults (35-65)"]
    dffMen = dff[dff["Group"] == "Men (18-34)"]
    dffWomen = dff[dff["Group"] == "Women (18-34)"]

    #Create a barchart, with a colorcoded bar for each racial group.
    fig = go.Figure(data=[
        go.Bar(name='Women (18-34)', x=dffWomen['Year'], y=dffWomen['Median Income'], marker_color='#dd3430'),
        go.Bar(name='Men (18-34)', x=dffMen['Year'], y=dffMen['Median Income'], marker_color='#3c90ce'),
        go.Bar(name='Adults (35-65)', x=dffAdults['Year'], y=dffAdults['Median Income'], marker_color='#2c3e65'),
    ])

    #Update the hover menu to only display the median weekly income.
    fig.update_traces(hovertemplate='Median Weekly Income: $%{y:.2f}')
    fig.update_traces(hoverinfo='none')

    #Set the aesthetic characteristics of the barchart.
    fig.update_layout(xaxis_title="Year", yaxis_title="Median Weekly Income", showlegend=True, hoverlabel=dict(
        font_size=10,
        font_family="Arial, serif"
    ))
    fig.layout.yaxis.tickformat = '$.0f'
    fig.layout.font.color='#2c3e65'
    fig.update_layout(font=dict(
        family="Arial, serif",
        size=14,
    ))


    return container, fig

#Command that ensures dash capabilities are enabled.
#This allows the code to be deployed on an online server.
# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
