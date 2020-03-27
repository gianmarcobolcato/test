import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
# import plotly.express as px


import numpy as np


app = dash.Dash(__name__)
server = app.server

app.css.append_css({'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'})

df=pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',sep=',')
df=df.drop(8781)
available_indicators=df['Country'].unique()





w=pd.read_csv('https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-province/dpc-covid19-ita-province.csv',sep=',')
available_regions=w['denominazione_regione'].unique()





trace1 = [dict(type='scattermapbox',
                lon = w['long'],
                lat = w['lat'],
                text=w['totale_casi'],
                mode='markers',
                marker = dict(
                size =w['totale_casi']/100,
                color='Red',
                opacity = 0.4,
                reversescale = True,
                autocolorscale = False,
                ))]
layout1 = dict(title='Contagion Map (fai zoom sulla tua regione!)',height=800,width=800, mapbox=dict(style='open-street-map',zoom=5,
                            center=dict(lat=42,lon=12),
                            ))
fig=dict(data=trace1,layout=layout1)





app.layout = html.Div([
    html.Div([

        html.Div([html.P("Hi DISHUNTER! Questi grafici ti aiuteranno a capire come si sta espandendo Covid-19! Divertiti! "),
            html.Hr(),
            html.H1('World Contagion Recap'),
            html.P("Seleziona i Paesi che vuoi confrontare!"),
            dcc.Dropdown(
                id='world_dropdown',
                options=[{'label': i, 'value': i} for i in available_indicators],

                multi=True
            ),
        ],
            style={'width': '60%', 'display': 'inline-block'}),


    html.Div([
        dcc.Graph(
            id='world_cases',
# 'display': 'inline-block'
        )
    ],style={'width': '70%', 'padding': '0 20'}),

        html.Div([
        html.Hr(),
        html.Div(id="world_data"),
        html.Hr(),
        ],
        style={'width': '60%', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(
            id='world_deaths',

        )
    ], style={'width': '70%', 'padding': '0 20'}),

    html.Div([
    html.Hr(),
    html.H1('Italy Contagion Recap'),
        html.P("Seleziona le Regioni che vuoi confrontare!"),
        dcc.Dropdown(
            id='italy_dropdown',
            options=[{'label': i, 'value': i} for i in available_regions],

            multi=True
        ),
        dcc.Graph(
            id='italy_cases',
        ),
        html.Hr(),
        html.Div(id="italy_data"),
        html.Hr(),

        dcc.Graph(
            id='italy_map',figure=fig
        ),
        html.Hr(),
        html.P('Fai Double tap sul grafico se hai zoomato troppo (Si, proprio come quando metti mi piace su instagram)'),
        html.Hr(),
        ], style={'width': '70%', 'padding': '0 20'}),


])
])

@app.callback(
    dash.dependencies.Output('world_cases', 'figure'),
    [dash.dependencies.Input('world_dropdown', 'value')])
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
                marker=dict(
                size=10,
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
    dash.dependencies.Output('world_data', 'children'),
    [dash.dependencies.Input('world_dropdown', 'value')])
def update_graph(countries):

    df1=df[df['Country'].isin(countries)]
    dataTrace=[]
    for country in df1['Country'].unique():
        df2=df1[df1['Country']==country]
        cases=df2['Confirmed'].max()
        deaths=df2['Deaths'].max()
        death_rate=deaths/cases*100
        summary='[Ci sono {} casi e {} morti in {}, tasso di morte= {:.2f}% ]'.format(cases,deaths,country,death_rate)
        dataTrace.append(summary)

    return dataTrace








@app.callback(
    dash.dependencies.Output('world_deaths', 'figure'),
    [dash.dependencies.Input('world_dropdown', 'value')])
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

                    marker=dict(
                    size=10,
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
    dash.dependencies.Output('italy_cases', 'figure'),
    [dash.dependencies.Input('italy_dropdown', 'value')])
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



@app.callback(
    dash.dependencies.Output('italy_data', 'children'),
    [dash.dependencies.Input('italy_dropdown', 'value')])
def update_italy_data(regions):

    w1=w[w['denominazione_regione'].isin(regions)]
    dataTrace=[]
    for region in w1['denominazione_regione'].unique():
        w2=w1[w1['denominazione_regione']==region]
        cases=w2.iloc[-2,9]
        summary='[Ci sono: {} casi in {} ]'.format(cases,region)
        dataTrace.append(summary)

    return dataTrace



if __name__ == '__main__':
    app.run_server(debug=True)
