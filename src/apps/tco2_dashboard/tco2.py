from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from .figures import verra_vintage, verra_map, verra_project, pool_pie_chart


def create_content_toucan(df, df_retired, df_carbon, df_verra, df_verra_toucan, verra_fallback_note):

    if verra_fallback_note != "":
        on_vs_off_chain_row = dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.H2("Off-Chain Verra Credits vs On-Chain Verra Credits Analysis")),
                    dbc.CardFooter(
                        verra_fallback_note,
                        id="fallback_indicator")
                ]), width=12, style={'textAlign': 'center'}),
            style={'paddingTop': '60px'}
        )
    else:
        on_vs_off_chain_row = dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.H2("Off-Chain Verra Credits vs On-Chain Verra Credits Analysis")),
                ]), width=12, style={'textAlign': 'center'}),
            style={'paddingTop': '60px'}
        )

    content_tco2 = [
        dbc.Row(
            dbc.Col(
                dbc.Card([
                    dbc.CardHeader(
                        html.H1("State of Toucan Tokenized Carbon", className='page-title'))
                ]), width=12, style={'textAlign': 'center'})
        ),

        dbc.Row([
            dbc.Col(dbc.Card([
                html.H5("TCO2 Tonnes Bridged", className="card-title"),
                dbc.CardBody("{:,}".format(
                    int(df["Quantity"].sum())), className="card-text")
            ]), lg=4, md=12),
            dbc.Col(dbc.Card([
                html.H5("TCO2 Tonnes Retired", className="card-title"),
                dbc.CardBody("{:,}".format(
                    int(df_retired["Quantity"].sum())), className="card-text")
            ]), lg=4, md=12),
            dbc.Col(dbc.Card([
                html.H5("TCO2 Tonnes Outstanding",
                        className="card-title"),
                dbc.CardBody("{:,}".format(
                    int(df["Quantity"].sum()-df_retired["Quantity"].sum())), className="card-text")
            ]), lg=4, md=12),
        ], style={'paddingTop': '60px'}),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.H5("Breakdown of TCO2 Pooled",
                            className="card-title"),
                    dbc.CardBody(dcc.Graph(figure=pool_pie_chart(df_carbon)))
                ], className="card-graph")
            ], width=12),
            # TODO: add methodology filter for NCT before re-enabling
            # dbc.Col([
            #     dbc.Card([
            #         html.H5("Conversion to Eligible Ratio of a specific Carbon Pool",
            #                 className="card-title"),
            #         dbc.CardBody([dbc.Row([
            #             dbc.Col(
            #                 dcc.Dropdown(options=[{'label': 'BCT', 'value': 'BCT'},
            #                                       {'label': 'NCT', 'value': 'NCT'}], value='BCT',
            #                              id='pie_chart_summary', placeholder='Select Carbon Pool',
            #                              style=dict(font=dict(color='black'))), width=3),
            #             dbc.Col([dcc.Graph(id="eligible pie chart plot")], width=9)])
            #                       ])
            #     ], className="card-graph")
            # ], lg=6, md=12),
        ]),

        on_vs_off_chain_row,

        dbc.Row([
            dbc.Col(dbc.Card([
                html.H5("Verra Registry credits ever Issued",
                        className="card-title"),
                dbc.CardBody("{:,}".format(
                    int(df_verra["Quantity"].sum())), className="card-text")
            ]), lg=4, md=12),
            dbc.Col(dbc.Card([
                html.H5("Verra Registry credits Tokenized by Toucan",
                        className="card-title"),
                dbc.CardBody("{:,}".format(
                    int(df_verra_toucan["Quantity"].sum())), className="card-text")
            ]), lg=4, md=12),
            dbc.Col(dbc.Card([
                html.H5("Percentage of Tokenized Credits",
                        className="card-title"),
                dbc.CardBody("{:.2%}".format(
                    (df_verra_toucan["Quantity"].sum()/df_verra["Quantity"].sum())),
                    className="card-text")
            ]), lg=4, md=12),
        ]),

        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Card([
                html.H5("Distribution of Vintage Start Dates",
                        className="card-title"),
                dcc.Graph(figure=verra_vintage(df_verra, df_verra_toucan))
            ]), width=12),
            dbc.Col(),
        ]),

        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Card([
                html.H5("Credits Tokenized vs. Credits Issued by Origin", className="card-title"),
                dcc.Graph(figure=verra_map(df_verra, df_verra_toucan
                                           ))
            ]), width=12),
            dbc.Col(),
        ]),

        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Card([
                html.H5("Distribution of Project Types",
                        className="card-title"),
                dcc.Graph(figure=verra_project(df_verra, df_verra_toucan))
            ]), width=12),
            dbc.Col(),
        ]),

        dbc.Row([
            dbc.Col(),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H2("Deep Dive into TCO2")),
                    dbc.CardBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader(
                                        html.H5("Select Performance Range", className="card-title"),),
                                    dbc.CardBody([dcc.Dropdown(options=[{'label': 'Last 7 Days Performance',
                                                                        'value': 'Last 7 Days Performance'},
                                                                        {'label': 'Last 30 Days Performance',
                                                                        'value': 'Last 30 Days Performance'},
                                                                        {'label': 'Lifetime Performance',
                                                                        'value': 'Lifetime Performance'}],
                                                               value='Lifetime Performance', id='summary_type',
                                                               placeholder='Select Summary Type')])
                                ])
                            ], lg=6, md=12),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardHeader(
                                        html.H5("Bridged or Retired TCO2s?", className="card-title"),),
                                    dbc.CardBody([dcc.Dropdown(options=[{'label': 'Bridged', 'value': 'Bridged'},
                                                                        {'label': 'Retired', 'value': 'Retired'}],
                                                               value='Bridged', id='bridged_or_retired',
                                                               placeholder='Select Summary Type')])
                                ])
                            ], lg=6, md=12),
                        ])
                    ])
                ]),
            ], width=12),
            dbc.Col()
        ], style={'paddingTop': '60px'}),


        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Card([
                dbc.CardBody(html.H2(id="Last X Days"),
                             style={'textAlign': 'center'})
            ]), lg=6, md=12),
            dbc.Col(),
        ]),

        dbc.Row([
            dbc.Col(dbc.Card([
                html.H5("Volume Over Time", className="card-title"),
                dcc.Graph(id="volume plot")
            ]), lg=6, md=12),
            dbc.Col(dbc.Card([
                html.H5("Distribution of Vintage Start Dates",
                        className="card-title"),
                dcc.Graph(id="vintage plot")
            ]), lg=6, md=12),
        ]),

        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Card([
                html.H5("Origin of Tokenized Credits", className="card-title"),
                dcc.Graph(id="map")
            ]), width=12),
            dbc.Col(),
        ]),

        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Card([
                html.H5("Distribution of Methodologies",
                        className="card-title"),
                dcc.Graph(id="methodology")
            ]), width=12),
            dbc.Col(),
        ]),

        dbc.Row([
            dbc.Col(),
            dbc.Col(dbc.Card([
                html.H5("Distribution of Projects", className="card-title"),
                dcc.Graph(id="projects")
            ]), width=12),
            dbc.Col(),
        ]),

        dbc.Row([], style={'paddingTop': '96px'})
    ]
    return content_tco2
