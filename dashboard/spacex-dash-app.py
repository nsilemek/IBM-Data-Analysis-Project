import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36','font-size': 40}),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] +
                [{'label': s, 'value': s} for s in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={int(min_payload): str(int(min_payload)),int(max_payload): str(int(max_payload))},
        value=[min_payload, max_payload]
    ),
    html.Br(),
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

@app.callback(Output('success-pie-chart', 'figure'), Input('site-dropdown', 'value'))
def update_pie(site):
    if site == 'ALL':
        df = spacex_df[spacex_df['class'] == 1]
        return px.pie(df, names='Launch Site', title='Total Successful Launches by Site')
    df = spacex_df[spacex_df['Launch Site'] == site]
    return px.pie(df, names='class', title=f'Success vs Failure for {site}')

@app.callback(Output('success-payload-scatter-chart', 'figure'),
              [Input('site-dropdown','value'),Input('payload-slider','value')])
def update_scatter(site,pl):
    low,high = pl
    df = spacex_df[(spacex_df['Payload Mass (kg)']>=low)&(spacex_df['Payload Mass (kg)']<=high)]
    if site != 'ALL': df = df[df['Launch Site']==site]
    return px.scatter(df, x='Payload Mass (kg)', y='class', color='Booster Version Category',
                      title=f'Payload vs Outcome ({site})')

if __name__ == '__main__':
    app.run(debug=True)
