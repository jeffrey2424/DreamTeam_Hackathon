from io import StringIO

from dash import Dash, html, dcc, Output, Input
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd

from google.cloud import storage


app = Dash(__name__)

colours = {
    'background': '#00864F',
    'text': '#FFFFFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


def read_blob_as_csv(bucket_name, file_name):
    client = storage.Client()

    bucket = client.get_bucket(bucket_name)
    file = StringIO(bucket.get_blob(file_name).download_as_string().decode('utf-8'))
    return pd.read_csv(file)


df_companies = read_blob_as_csv('hackathon-team-10-company-lists', "company_name_mappings.csv")
df_stocks = read_blob_as_csv('hackathon-team-10-ticker-data', "20220406_1d_nasdaq.csv")
df_events = read_blob_as_csv('hackathon-team-10-test-data', "fake_gdelt_out.csv")


app.layout = html.Div(
    children=[
        html.H1(children='Company Stock Checker', style={"color": colours["text"], 'textAlign': 'center'}),
        html.Br(),
        html.Div(
            children="Select a company to check",
            style={"color": colours["text"], 'textAlign': 'left'}
        ),
        dcc.Dropdown(
            id="slct_comp",
            options={row[1]["Code"]: row[1]["Name"] for row in df_companies.iterrows()},
            multi=False,
            style={'width': "40%"},
            value="GOOG"
        ),
        dcc.Graph(
            id="stock_graph",
            figure={}
        )
    ],
    style={
        "width": "100%",
        "height": "100vh",
        "backgroundColor": colours["background"],
        "font-family": 'Arial'
    }
)


@app.callback(
    Output(component_id='stock_graph', component_property='figure'),
    Input(component_id='slct_comp', component_property='value')
)
def generate_stockgraph_and_events(company_code: str):
    fig = make_subplots()
    fig.add_trace(get_stock_line(company_code))
    plt_good, plt_bad = get_events_scatter(company_code)
    fig.add_trace(plt_good)
    fig.add_trace(plt_bad)
    return fig


def get_stock_line(company_code):
    df = df_stocks[df_stocks["Company"] == company_code]
    return go.Line(x=df["Date"], y=df["Close"])


def get_events_scatter(company_code):
    company_name = df_companies[df_companies["Code"] == company_code]["Name"].iloc[0]
    df_e = df_events[df_events["Company"] == company_name]
    df_s = df_stocks[df_stocks["Company"] == company_code]

    df_comb = pd.merge(df_e, df_s, how='inner', on="Date")
    df_good = df_comb[df_comb["SentimentScore"] > 0]
    df_bad = df_comb[df_comb["SentimentScore"] < 0]

    plt_good = go.Scatter(
        x=df_good["Date"],
        y=df_good["Close"],
        marker=dict(
            color='Green',
            size=15,
            symbol=5,
            opacity=0.7,
            ),
        mode='markers'
        )
    plt_bad = go.Scatter(
        x=df_bad["Date"],
        y=df_bad["Close"],
        marker=dict(
            color='Red',
            size=15,
            symbol=6,
            opacity=0.7,
        ),
        mode='markers'
    )
    return plt_good, plt_bad


if __name__ == '__main__':
    app.run_server(debug=True, host='localhost')
