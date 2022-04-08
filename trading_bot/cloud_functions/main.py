import alpaca_trade_api as tradeapi
import config
from google.cloud.sql.connector import Connector
import sqlalchemy
import os
from datetime import datetime

# initialize Connector object
connector = Connector()


# def _getconn():
#     conn = connector.connect(
#         "hackathon-team-10:us-central1:ui-backend-test",
#         "pg8000",
#         user="postgres",
#         password="test",
#         db="postgres"
#     )
#     return conn


pool = sqlalchemy.create_engine(
    drivername="postgresql+pg8000://",
    username="postgres",
    password="test",
    database="postgres",
    query={
        "unix_sock": "/cloudsql/hackathon-team-10:us-central1:ui-backend-test.s.PGSQL.5432"
    }

)


def trade_stock(req):

    data = req.get_json()

    bq_run_time = data['bq_run_time']

    print(f'BQ TIME IS {bq_run_time}')


    print('setting up trade api')
    api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL)
    print('trade api is set up')

    print('loading from company mappings dict')
    # Load in the company name mappings
    c_map = _load_company_mappings()
    print('company mappings table loaded')


    # read the new gdelt info / need a timestamp
    latest_gdelt_events = _load_latest_gdelt_events(bq_run_time)

    # make trades

    orders = []

    for row in latest_gdelt_events:
        print(row)
        print('-------')

        article_url, _, _, mid, _, _, sent, _, _, _ = row

        symbol = c_map[mid]
        trade = 'buy' if sent > 0.5 else 'sell'

        try:
            order = api.submit_order(
                symbol,
                10,
                trade,
                'market',
                'gtc'
            )
            orders.append(order)
        except Exception as e:
            pass

        try:            
            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            _insert_trades_made(date = now, ticker = symbol, trade = trade, quantity=10, url=article_url)
        except Exception as e:
            pass



    return {
        'code': 'success',
    }


def _load_company_mappings():
    with pool.connect() as db_conn:
        # query database
        result = db_conn.execute("SELECT * FROM main.company_mappings_mid").fetchall()

        d = {row[4]: row[1] for row in result}

        return d


def _load_latest_gdelt_events(bq_run_time):
    with pool.connect() as db_conn:
        # query database
        result = db_conn.execute(f"SELECT * FROM gdelt_events_2 WHERE bq_run_time > {bq_run_time}").fetchall()

        return result


def _insert_trades_made(date, ticker, trade, quantity, url):
    with pool.connect() as db_conn:
        # Insert orders placed
        q = f"""
            INSERT INTO main.alpaca_trades(Date, Ticker, Trade, Quantity, url)
            VALUES ('{date}', '{ticker}', '{trade}', {quantity}, '{url}');
        """
        db_conn.execute(q)