import sqlalchemy
from google.cloud.sql.connector import Connector
import pg8000
import pandas as pd


class SQLConnection:

    def __init__(self, connection_name, db):
        self._connection_name = connection_name
        self._db = db

    def _init_connection_engine(self) -> sqlalchemy.engine.Engine:
        def getconn() -> pg8000.dbapi.Connection:
            with Connector() as connector:
                conn = connector.connect(
                    self._connection_name,
                    "pg8000",
                    # user="hackthon-team-10-cloud-sql@hackathon-team-10.iam.gserviceaccount.com",
                    user="postgres",
                    password="test",
                    db=self._db,
                )
            return conn

        engine = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=getconn,
        )
        engine.dialect.description_encoding = None
        return engine

    def run_qry(self, qry):
        pool = self._init_connection_engine()
        df = pd.read_sql_query(qry, con=pool)
        return df

    def run_nonqry(self, qry):
        pool = self._init_connection_engine()
        with pool.connect() as conn:
            response = conn.execute(qry)
        return response
