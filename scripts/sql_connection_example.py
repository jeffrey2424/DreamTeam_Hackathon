from src.io.sql import SQLConnection


if __name__ == "__main__":
    conn = SQLConnection(
        connection_name="hackathon-team-10:us-central1:ui-backend-test",
        db="postgres"
    )

    result = conn.run_qry("SELECT * FROM main.gdelt_events_coded limit 10;")
    # result = conn.run_qry("select table_schema, count(*) from information_schema.tables group by table_schema;")
    # result = conn.run_qry("select * from information_schema.tables where table_schema = 'main';")
    # print(result)
    for schema, name in zip([result["table_schema"], result["table_name"]]):
        print(schema, name)
