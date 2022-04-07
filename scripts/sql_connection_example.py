from src.io.sql import SQLConnection

conn = SQLConnection(
    connection_name="hackathon-team-10:us-central1:ui-backend-test",
    db="gdelt_sustainability"
)

result = conn.run_qry("select * from information_schema.tables")

print(result)