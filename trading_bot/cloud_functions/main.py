import alpaca_trade_api as tradeapi
import config
from google.cloud.sql.connector import Connector
import sqlalchemy

# initialize Connector object
connector = Connector()


def _getconn():
    conn = connector.connect(
        "hackathon-team-10:us-central1:ui-backend-test",
        "pg8000",
        user="postgres",
        password="test",
        db="postgres"
    )
    return conn


pool = sqlalchemy.create_engine(
    "postgresql+pg8000://",
    creator=_getconn,
)


def trade_stock(req):
    data = req.get_json()

    api = tradeapi.REST(config.API_KEY, config.SECRET_KEY, config.BASE_URL)

    # Load in the company name mappings
    c_map = _load_company_mappings()

    # read the new gdelt info / need a timestamp
    latest_gdelt_events = _load_latest_gdelt_events()

    # make trades

    orders = []

    for row in latest_gdelt_events:
        url, date, corpus_s, sent_s, company, time, id = row
        symbol = c_map[company]

        try:
            order = api.submit_order(
                symbol,
                10,
                'buy' if sent_s > 0.5 else 'sell',
                'market',
                'gtc'
            )
            orders.append(order)
        except Exception as e:
            pass

    return {
        'code': 'success',
        'order_id': order.id,
        'order_status': order.status
    }


def _load_company_mappings():
    with pool.connect() as db_conn:
        # query database
        result = db_conn.execute("SELECT * FROM main.company_mappings_mid").fetchall()

        d = {row[0]: row[1] for row in result}

        return d


def _load_latest_gdelt_events():
    with pool.connect() as db_conn:
        # query database
        result = db_conn.execute("SELECT * FROM test2.gdelt_out LIMIT 3").fetchall()

        return result