import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import numpy as np

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SLATE],
                meta_tags=[
                    {
                        'name': 'description',
                        'content': '''
                               A Fantasy Premier League (FPL) dashboard
                               which allows users to plot several key
                               performance metrics against each other
                               which allows users to obtain key
                               insights on the statistical indicators of top
                               players in the Premier League (EPL).
                    
                               '''
                    },

                    {
                        'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'
                    },

                    {
                        'http-equiv': 'X-UA-Compatible',
                        'content': 'IE=edge'
                     },

                ]
                )

server = app.server

df = pd.read_csv('./data/combined_df.csv')

metrics = sorted(df.loc[:, 'Minutes':].columns)
teams = sorted(df['Team'].unique())
positions = [(1, 'GKP'),
             (2, 'DEF'),
             (3, 'MID'),
             (4, 'FWD')]

app.layout = html.Div([
    html.H1('2-D Player Comparison',
            style={'text-align': 'center'}),
    html.Br(),
    html.Div([
        dcc.Markdown("""
            **Purpose**

            A Fantasy Premier League (FPL) dashboard
            which allows users to plot several key
            performance metrics against each other
            which allows users to obtain key
            insights on the statistical indicators of top
            players in the Premier League (EPL).
        """),
    ],
    style={'display': 'block',
           'marginLeft': 'auto',
           'marginRight': 'auto',
           'width': '25%'
    }),
    html.Br(),
    dcc.Graph(id='metric-graph',
              responsive=True,
              config={
                  'scrollZoom': True,
                  'modeBarButtonsToRemove': [
                      'select2d',
                      'lasso2d',
                      'zoomIn2d',
                      'zoomOut2d',
                      'hoverClosestCartesian',
                      'hoverCompareCartesian'
                  ],
                  'displaylogo': False,
                  'watermark': False,
              },
              style={'background-color': '#52575C',
                       'display': 'block',
                       'margin': 'auto',
                       'position': 'relative'}),
    html.Br(),
    html.Div([
        html.Div([
            html.H2('Metrics',
            style={'text-align': 'center'}),
            html.P('x-axis metric'),
            dcc.Dropdown(
                id='xaxis-column',
                options=[{'label': i, 'value': i} for i in metrics],
                value='ICT Index',
                clearable=False,
                searchable=False,
                persistence_type='session',
                persistence=True,
                style={'background-color': '#52575C',
                       'display': 'block',
                       'margin': 'auto'}
            ),
            html.P('y-axis metric'),
            dcc.Dropdown(
                id='yaxis-column',
                options=[{'label': i, 'value': i} for i in metrics],
                value='Total Points',
                clearable=False,
                searchable=False,
                persistence_type='session',
                persistence=True,
                style={'background-color': '#52575C',
                       'display': 'block',
                       'margin': 'auto'}
            ),
        ],
        style={'display': 'inline-block',
               'margin':'0 0 0',
               'width': '50%',
               'paddingLeft': '10vw',
               'paddingRight': '10vw'}),
        
        html.Div([
            html.H2('Filters',
            style={'text-align': 'center'}),
            html.P('Team Filter'),
            dcc.Dropdown(
                id='team-filter',
                options=[{'label': i, 'value': i} for i in teams],
                clearable=True,
                searchable=False,
                multi=True,
                persistence_type='session',
                persistence=True,
                style={'background-color': '#52575C',
                       'display': 'block',
                       'margin': 'auto',
                       'position': 'relative'}
            ),
            html.P('Position Filter'),
            dcc.Dropdown(
                id='position-filter',
                options=[{'label': v, 'value': k} for k, v in positions],
                clearable=True,
                searchable=False,
                multi=True,
                persistence_type='session',
                persistence=True,
                style={'background-color': '#52575C',
                       'position': 'relative'}
            )
        ],
        style={'display': 'inline-block',
               'margin': '0 0 0',
               'width': '50%',
               'paddingLeft': '10vw',
               'paddingRight': '10vw'}),

        html.Br(),

    ],
    id='dropdown',
    style={'display': 'flex',
           'flex-direction': 'row',
           'float': 'center',
           'align-items': 'center',
           'position': 'relative',}
    ),
],
)


@app.callback(
    Output('metric-graph', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('team-filter', 'value'),
     Input('position-filter', 'value')])
def update_graph(xaxis,
                 yaxis,
                 team_filter,
                 pos_filter):
    if team_filter:
        filtered_df = df[df['Team'].isin(team_filter)]
    else:
        filtered_df = df

    if pos_filter:
        filtered_df = filtered_df[filtered_df['Position'].isin(pos_filter)]

    fig = px.scatter(filtered_df,
                     x=xaxis,
                     y=yaxis,
                     hover_name='player_name',
                     hover_data={
                         'player_name': False
                     },
                     text='player_name',
                     color='Team',
                     size=np.maximum(filtered_df['Total Points'], 0),
                     render_mode='gl',
                     labels=dict(x=str(xaxis),
                                 y=str(yaxis),
                                 color='Team',
                                 size='Total Points')
                     )

    fig.update_traces(textposition='top right', showlegend=False)
    fig.update_xaxes(title=xaxis,
                     title_font_size=20,
                     showgrid=False,
                     zeroline=False)
    fig.update_yaxes(title=yaxis,
                     title_font_size=20,
                     showgrid=False,
                     zeroline=False)
    fig.update_layout(title={'text': f'{xaxis} vs. {yaxis}',
                             'font': {'size': 32},
                             'x': 0.5
                             },
                      autosize=True,
                      hovermode='closest',
                      plot_bgcolor='#1F242D',
                      paper_bgcolor='#272B30',
                      font_color='#A3791C')

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
