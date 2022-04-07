import time
from pprint import pprint
from googleapiclient import discovery
from oauth2client.client import GoogleCredentials


def hello_gcs(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print(f"Processing file: {event['name']}.")

    credentials = GoogleCredentials.get_application_default()
    uri = f"gs://{event['bucket']}/{event['name']}"
    db = "postgres"
    tbl = "gdelt_events_2"
    service = discovery.build('sqladmin', 'v1beta4', credentials=credentials)

    # Project ID of the project that contains the instance.
    project = 'hackathon-team-10'  # TODO: Update placeholder value.

    # Cloud SQL instance ID. This does not include the project ID.
    instance = 'ui-backend-test'  # TODO: Update placeholder value.

    body = {
        "importContext": {
          "uri": uri,
          "database": db,
          "kind": "sql#importContext",
          "fileType": "CSV",
          "csvImportOptions": {
            "table": tbl,
          },
        }
    }
    request = service.instances().import_(project=project, instance=instance, body=body)
    response = request.execute()

    # TODO: Change code below to process the `response` dict:
    pprint(response)

    # TODO: Actually wait for the operation to end
    # See https://cloud.google.com/sql/docs/mysql/admin-api/rest/v1beta4/instances/import
    # See https://cloud.google.com/sql/docs/mysql/admin-api/rest/v1beta4/operations#Operation
    time.sleep(30)
