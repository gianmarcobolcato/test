import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
%matplotlib inline
from ipywidgets import interact, interact_manual
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

app = dash.Dash(__name__)
server = app.server

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

df=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',sep=',')
available_indicators=df['Country'].unique()

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                #value='Fertility rate, total (births per woman)'
            ),
            dcc.Dropdown(
                id='crossfilter-xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                #value='Fertility rate, total (births per woman)'
            ),
        ],
            style={'width': '49%', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
])
])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column1', 'value'),
    dash.dependencies.Input('crossfilter-xaxis-column2', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name):
    df1=df[df['Country']==[xaxis_column_name]
    df2=df[df['Country']==[yaxis_column_name]


    return {
        'data': [go.Scatter(
            x=df1['Date'],
            y=df1['Confirmed'],
            text=df1['Country'],
            #customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear' if xaxis_type == 'Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear' if yaxis_type == 'Linear' else 'log'
            },
            margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
            height=450,
            hovermode='closest'
        )
    }


# def create_time_series(dff, axis_type, title):
#     return {
#         'data': [go.Scatter(
#             x=dff['Year'],
#             y=dff['Value'],
#             mode='lines+markers'
#         )],
#         'layout': {
#             'height': 225,
#             'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
#             'annotations': [{
#                 'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
#                 'xref': 'paper', 'yref': 'paper', 'showarrow': False,
#                 'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
#                 'text': title
#             }],
#             'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
#             'xaxis': {'showgrid': False}
#         }
#     }
#
#
# @app.callback(
#     dash.dependencies.Output('x-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
# def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
#     country_name = hoverData['points'][0]['customdata']
#     dff = df[df['Country Name'] == country_name]
#     dff = dff[dff['Indicator Name'] == xaxis_column_name]
#     title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
#     return create_time_series(dff, axis_type, title)
#
#
# @app.callback(
#     dash.dependencies.Output('y-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
# def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
#     dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
#     dff = dff[dff['Indicator Name'] == yaxis_column_name]
#     return create_time_series(dff, axis_type, yaxis_column_name)
#

if __name__ == '__main__':
    app.run_server(debug=True)
