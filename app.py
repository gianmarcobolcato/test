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

        html.Div([
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
    ], style={'width': '49%', 'padding': '0 20'}),
        html.Hr(),
        html.Div(id="number-out"),
        html.Hr(),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter2',

        )
    ], style={'width': '49%', 'padding': '0 20'}),
    html.Div([
        html.P("Select the countries you want to compare"),
        dcc.Dropdown(
            id='crossfilter-xaxis-column3',
            options=[{'label': i, 'value': i} for i in available_regions],

            multi=True
        ),
        dcc.Graph(
            id='crossfilter-indicator-scatter3',
        )])
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
        trace =go.Scattergeo(
            lon = w2['long'],
            lat = w2['lat'],
            name=region,
            mode = 'markers',
            marker = dict(
            size = w2['totale_casi']/100,
            opacity = 0.8,
            reversescale = True,
            autocolorscale = False,
            )
        )

        dataTrace.append(trace)

    layout =go.Layout(
            title = 'Italy map Contagion',
            geo = dict(
            scope='europe',
            projection_type='natural earth',
            showland = True,
            landcolor = 'rgb(115, 115, 115)',
            subunitcolor = "rgb(217, 217, 217)",
            countrycolor = "rgb(150, 150, 150)",
            countrywidth = 0.5,
            subunitwidth = 0.5,
        ),
            width=1000,
            height=800
    )
    fig = dict(data=dataTrace, layout=layout)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
