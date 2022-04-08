from io import StringIO

from dash import Dash, html, dcc, Output, Input, dash_table
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi

from google.cloud import storage

from src.io.shh import SecretManager

secret_manager = SecretManager("hackathon-team-10")

API_KEY = secret_manager.get_secret("BOT_API_KEY")
SECRET_KEY = secret_manager.get_secret("BOT_SECRET_KEY")
BASE_URL = 'https://paper-api.alpaca.markets'
LAST_PORTFOLIO_VALUE = 0

from src.io.sql import SQLConnection


conn = SQLConnection(
        connection_name="hackathon-team-10:us-central1:ui-backend-test",
        db="postgres"
    )


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    meta_tags=[
        {'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}
    ]
)

api = tradeapi.REST(API_KEY, SECRET_KEY, BASE_URL)


colours = {
    'background': '#ccffcc',
    'text': '#000000'
}

LOGO_URL = "https://storage.googleapis.com/london_wall_street_bets/London%20Wall%20Street%20Bets%20Scenic.png"

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


def read_blob_as_csv(bucket_name, file_name):
    client = storage.Client()

    bucket = client.get_bucket(bucket_name)
    file = StringIO(bucket.get_blob(file_name).download_as_string().decode('utf-8'))
    return pd.read_csv(file)


# df_companies1 = read_blob_as_csv('hackathon-team-10-company-lists', "company_name_mappings.csv")
df_companies = conn.run_qry("SELECT * FROM main.company_mappings_mid;")

# df_stocks1 = read_blob_as_csv('hackathon-team-10-ticker-data', "20220406_1d_nasdaq.csv")
df_stocks = conn.run_qry("SELECT * FROM main.nasdaq_history;")

# df_events1 = read_blob_as_csv('hackathon-team-10-test-data', "fake_gdelt_out.csv")
df_events = conn.run_qry("""
    SELECT  
        date,
        code,
        name,
        case when sentiment_score > 0 then 'buy' else 'sell' end as action,
        corpus_score,
        sentiment_score,
        close as price
    FROM 
        main.stock_events
    WHERE
        corpus_score > 0.01
        AND (sentiment_score > 0.01 OR sentiment_score < -0.01)
    ORDER BY
        date desc;
    """)
df_events["corpus_score"] = df_events["corpus_score"].round(2)

app.layout = dbc.Container(
    [
        dbc.Container(
            dbc.Row(
                [
                    dbc.Col(html.H1(children='London Wall Street Bets Stock Checker', style={"color": colours["text"], 'textAlign': 'left', 'margin-top': 45}), width=8),
                    dbc.Col(html.Img(src=LOGO_URL, style={'height': '100%', 'width': '100%'}), width={'size': 2, 'offset': 2}),
                ],
                className='border border-dark',
                style={"backgroundColor": "#00864F"},
            ),
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(
                                    children="Select a company to check",
                                    style={"color": colours["text"], 'textAlign': 'left'}
                                ),
                                dcc.Dropdown(
                                    id="slct_comp",
                                    options={row[1]["code"]: row[1]["gkg_name"] for row in df_companies.iterrows()},
                                    multi=False,
                                    # style={'width': "40%"},
                                    value="GOOG"
                                ),
                            ],
                            width={'size': 5}
                        ),
                        dbc.Col(
                            [
                                dcc.Interval(id='portfolio_value_interval', interval=5000),
                                html.H2(id='portfolio_value', children=''),
                            ],
                            width={'size': 7}
                        ),
                    ],
                    style={'margin-top': 45},
                    # width={'size': 7}
                    # style={"backgroundColor": "#00864F"},
                    # no_gutters=True
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dash_table.DataTable(
                                data=df_events.to_dict('records'),
                                columns=[{"name": i, "id": i} for i in df_events.columns],
                                page_size=14,
                                style_data={
                                    'whiteSpace': 'normal',
                                    'height': 'auto',
                                },
                                style_cell={'fontSize':10, 'font-family':'Arial'},
                            ),
                            width={'size': 5}
                        ),
                        dbc.Col(
                            [
                                dcc.Graph(
                                    id="stock_graph",
                                    figure={},
                                )
                            ],
                            width={'size': 7}
                        ),
                    ],
                    # style={"backgroundColor": "#00864F"},
                    # no_gutters=True
                    style={'margin-top': 45, 'margin-bottom': 45},
                ),
            ],
            style={"backgroundColor": colours["background"]},
            className='border border-dark',
            # fluid=False,
        ),
    ],
    style={
        "width": "100%",
        "height": "100vh",
        # "backgroundColor": colours["background"],
        "font-family": 'Arial'
    }
)


@app.callback(Output('portfolio_value', 'children'),
              [Input('portfolio_value_interval', 'n_intervals')]
              )
def get_portfolio_value(n):
    global LAST_PORTFOLIO_VALUE
    equity = api.get_portfolio_history(period='1D', timeframe='1D').equity[-1]
    header = html.H1(
        children=f"Portfolio Value: £{int(equity)}",
        style={
            'color': "Green" if equity >= LAST_PORTFOLIO_VALUE else "Red",
            'textAlign': 'center'
        }
    )
    LAST_PORTFOLIO_VALUE = equity
    return header


@app.callback(
    Output(component_id='stock_graph', component_property='figure'),
    Input(component_id='slct_comp', component_property='value')
)
def generate_stockgraph_and_events(company_code: str):
    df = conn.run_qry(f"SELECT * FROM main.stock_events WHERE code = '{company_code}'")
    fig = make_subplots()
    fig.add_trace(get_stock_line(df))
    plt_good, plt_bad = get_events_scatter(df)
    fig.add_trace(plt_good)
    fig.add_trace(plt_bad)
    return fig


def get_stock_line(df):
    return go.Line(x=df["date"], y=df["close"], name="Stock", showlegend=False)


def get_events_scatter(df):
    df_good = df[df["sentiment_score"] > 0]
    df_bad = df[df["sentiment_score"] < 0]

    plt_good = go.Scatter(
        x=df_good["date"],
        y=df_good["close"],
        marker=dict(
            color='Green',
            size=15,
            symbol=5,
            opacity=0.7,
            ),
        mode='markers',
        name="Good Sustainability Event",
        showlegend = False,
        )
    plt_bad = go.Scatter(
        x=df_bad["date"],
        y=df_bad["close"],
        marker=dict(
            color='Red',
            size=15,
            symbol=6,
            opacity=0.7,
        ),
        mode='markers',
        name="Bad Sustainability Event",
        showlegend=False,
    )
    return plt_good, plt_bad


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
