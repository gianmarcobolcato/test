import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd



import numpy as np


app = dash.Dash(__name__)
server = app.server

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

df=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',sep=',')
available_indicators=df['Country'].unique()


w=pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv',sep=',')
available_regions=w['denominazione_regione'].unique()


app.layout = html.Div([
    html.Div([

        html.Div([html.P("Hi DISHUNTER! These Graphs will help you to understand how COVID19 is spreading! Enjoy! "),
            html.Hr(),
            html.H1('World contagion recap'),
            html.P("Select the countries you want to compare"),
            dcc.Dropdown(
                id='crossfilter-xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],

                multi=True
            ),
        ],
            style={'width': '49%', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
# 'display': 'inline-block'
        )
    ], style={'width': '55%', 'padding': '0 20'}),
        html.Hr(),
        html.Div(id="number-out"),
        html.Hr(),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter2',

        )
    ], style={'width': '55%', 'padding': '0 20'}),
    html.Hr(),
    html.Div([html.H1('Italy contagion recap'),
        html.P("Select the italian regions you want to compare"),
        dcc.Dropdown(
            id='crossfilter-xaxis-column3',
            options=[{'label': i, 'value': i} for i in available_regions],

            multi=True
        ),
        dcc.Graph(
            id='crossfilter-indicator-scatter3',
        )

        ], style={'width': '55%', 'padding': '0 20'}),
        html.Hr(),
        html.Div(id="number-out2"),
        html.Hr(),
])
])

@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column1', 'value')])
def update_graph(countries):
        # filtered_ddf_item_in = ddf_item_in[ddf_item_in['ITEMCODE'].isin(selected_ITEM)]
    df1=df[df['Country'].isin(countries)]
    dataTrace=[]
    for country in df1['Country'].unique():
        df2=df1[df1['Country']==country]
        trace = go.Scatter(
                x=df2['Date'],
                y=df2['Confirmed'],
                name=country,
                mode='lines + markers',
                opacity=0.6,
                marker=dict(
                size=8,
                symbol='circle',
                )
                    )

        dataTrace.append(trace)


    layout =go.Layout(
        title='Cumulative Trend Cases' ,
        autosize= True,
        hovermode= "closest",
        scene= dict(
            xaxis=dict(title='date',showgrid=True, zeroline=False,  ticks='', showticklabels=True, showline=True, linewidth=1, linecolor='orange', mirror=True),
            yaxis=dict(title='cases',showgrid=True, zeroline=False, ticks='', showticklabels=True, showline=True, linewidth=1, linecolor='orange', mirror=True),

        ),
        #width=500,
        #height=500
        )
    fig = dict(data=dataTrace, layout=layout)
    return fig




@app.callback(
    dash.dependencies.Output('number-out', 'children'),
    [dash.dependencies.Input('crossfilter-xaxis-column1', 'value')])
def update_graph(countries):

    df1=df[df['Country'].isin(countries)]
    dataTrace=[]

    for country in df1['Country'].unique():
        df2=df1[df1['Country']==country]
        print(df2)
        cases=df2['Confirmed'].max()
        deaths=df2['Deaths'].max()
        death_rate=deaths/cases*100
        summary='[There are {} cases and {} deaths in {}, death_rate= {:.2f}% ]'.format(cases,deaths,country,death_rate)
        dataTrace.append(summary)

    return dataTrace








@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter2', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column1', 'value')])
def update_graph2(countries):
            # filtered_ddf_item_in = ddf_item_in[ddf_item_in['ITEMCODE'].isin(selected_ITEM)]
    df1=df[df['Country'].isin(countries)]
    dataTrace=[]
    for country in df1['Country'].unique():
        df2=df1[df1['Country']==country]
        trace = go.Scatter(
                    x=df2['Date'],
                    y=df2['Deaths'],
                    name=country,
                    mode='lines + markers',
                    opacity=0.6,
                    marker=dict(
                    size=8,
                    symbol='circle',
                    )
                        )

        dataTrace.append(trace)


    layout =go.Layout(
            title='Cumulative Trend Deaths' ,
            autosize= True,
            hovermode= "closest",
            scene= dict(
                xaxis=dict(title='date',showgrid=True, zeroline=False,  ticks='', showticklabels=True, showline=True, linewidth=1, linecolor='orange', mirror=True),
                yaxis=dict(title='deaths',showgrid=True, zeroline=False, ticks='', showticklabels=True, showline=True, linewidth=1, linecolor='orange', mirror=True),

            ),
            #width=500,
            #height=500
            )
    fig = dict(data=dataTrace, layout=layout)
    return fig





@app.callback(
    dash.dependencies.Output('crossfilter-indicator-scatter3', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column3', 'value')])
def update_graph3(regions):

    w1=w[w['denominazione_regione'].isin(regions)]
    dataTrace=[]
    for region in w1['denominazione_regione'].unique():
        w2=w1[w1['denominazione_regione']==region]
        trace =go.Bar(
            x = w2['data'],
            y = w2['totale_casi'],
            name=region,
        )

        dataTrace.append(trace)

    layout =go.Layout(
            title='Covid19 cases by region (Italy)' ,
            autosize= True,
            hovermode= "closest",
            scene= dict(
                xaxis=dict(title='date',showgrid=True, zeroline=False,  ticks='', showticklabels=True, showline=True, linewidth=1, linecolor='orange', mirror=True),
                yaxis=dict(title='cases',showgrid=True, zeroline=False, ticks='', showticklabels=True, showline=True, linewidth=1, linecolor='orange', mirror=True),

            ),
            #width=500,
            #height=500
            )
    fig = dict(data=dataTrace, layout=layout)
    return fig



# @app.callback(
#     dash.dependencies.Output('number-out2', 'children'),
#     [dash.dependencies.Input('crossfilter-xaxis-column3', 'value')])
# def update_graph(regions):
#
#     w1=w[w['denominazione_regione'].isin(regions)]
#     dataTrace=[]
#     for region in w1['denominazione_regione'].unique():
#         w2=w1[w1['denominazione_regione']==region]
#         print(w2)
#         summary='[There are {} cases in {}'.format(cases,region)
#         dataTrace.append(summary)
#
#     return dataTrace





if __name__ == '__main__':
    app.run_server(debug=True)
