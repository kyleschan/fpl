import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

import pandas as pd
import numpy as np

# external CSS stylesheets
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.SLATE, external_stylesheets],
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
            style={'text-align': 'center',
                   'fontWeight': 'bold'}),
    html.Br(),
    html.Div([
        dcc.Markdown("""
            ** Purpose **

            A Fantasy Premier League (FPL) dashboard
            which allows users to plot several key
            performance metrics against each other
            which allows users to obtain key
            insights on the statistical indicators of top
            players in the Premier League (EPL).  Inform your
            next transfer by plotting any of the 50 different
            metrics, including [xG, xA](https://www.optasports.com/services/analytics/advanced-metrics/),
            and [VAPM](https://www.reddit.com/r/FantasyPL/comments/6r60fu/exploring_a_key_metric_value_added_per_1m/)
            to help discern high-value players from the rest of
            the pack.

            ** Features **
            - Filter the plot by maximum price, team, and
            position to find the player that best suits your team's
            needs.
            - Hover over points to reveal that individual player's
            exact values for the selected metrics.
            - Click and drag to zoom in on a portion of the graph;
            double-click to zoom out.
            - Select the Pan icon at the top right of the graph to
            toggle panning.
        """),
    ],
    style={'display': 'block',
           'marginLeft': 'auto',
           'marginRight': 'auto',
           'width': '75%'
    }),
    html.Br(),
    dcc.Graph(id='metric-graph',
              responsive=True,
              config={
                  'scrollZoom': False,
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
            html.P('Max Price (inclusive)'),
            dcc.Dropdown(
                id='price-cap',
                options=[{'label': i, 'value': i} for i in np.round(np.arange(4., 13., 0.1), 1)],
                clearable=True,
                searchable=False,
                persistence_type='session',
                persistence=True,
                style={'background-color': '#52575C',
                       'display': 'block',
                       'margin': 'auto',
                       'position': 'relative'}
            ),
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
                       'display': 'block',
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
           'position': 'relative'}
    ),
],
style={'overflow': 'scroll'}
)


@app.callback(
    Output('metric-graph', 'figure'),
    [Input('xaxis-column', 'value'),
     Input('yaxis-column', 'value'),
     Input('price-cap', 'value'),
     Input('team-filter', 'value'),
     Input('position-filter', 'value')])
def update_graph(xaxis,
                 yaxis,
                 price_cap,
                 team_filter,
                 pos_filter):

    # Apply filters
    filtered_df = df[(df['Cost'] / 10) <= price_cap] if price_cap else df
    filtered_df = filtered_df[filtered_df['Team'].isin(team_filter)] if team_filter else filtered_df
    filtered_df = filtered_df[filtered_df['Position'].isin(pos_filter)] if pos_filter else filtered_df

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
