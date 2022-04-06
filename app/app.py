from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

colours = {
    'background': '#00864F',
    'text': '#000000'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
# df_companies = pd.read_csv("companies.csv")
# df_stocks = pd.read_csv("fake_stock_price.csv")

# fig = px.line(df_stocks, x="Fruit", y="Amount", color="City",)

app.layout = html.Div(
    children=[
        html.H1(children='Company Stock Checker', style={"color": colours["text"]}),
        html.Br(),
    ],
)



if __name__ == '__main__':
    app.run_server(debug=True, port=8080, host='localhost')
