from io import StringIO

from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

from google.cloud import storage


app = Dash(__name__)

colours = {
    'background': '#00864F',
    'text': '#FFFFFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df_companies = pd.read_csv("../data/test_data/companies.csv")
# df_stocks = pd.read_csv("../data/test_data/fake_stock_price.csv")


def read_blob_as_csv(bucket_name, file_name):
    # try:
    client = storage.Client()
    # except:
    #     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\jeffr\Documents\Python\Hackathon\MainHack\DreamTeam_Hackathon\hackathon-team-10-6ca9ff276b51.json"
    #     client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    file = StringIO(bucket.get_blob(file_name).download_as_string().decode('utf-8'))
    return pd.read_csv(file)



df_companies = read_blob_as_csv('hackathon-team-10-test-data', "companies.csv")
df_stocks = read_blob_as_csv('hackathon-team-10-test-data', "fake_stock_price.csv")


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
            placeholder="Select a company...",
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
def generate_stockgraph(company_code: str):

    df = df_stocks[df_stocks["Code"] == company_code]

    fig = px.line(df, x="date", y="price")
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0')
