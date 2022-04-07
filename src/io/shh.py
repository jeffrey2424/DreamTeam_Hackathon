from google.cloud import secretmanager
import hashlib


class SecretManager:

    def __init__(self, project_id):
        self._project_id = project_id
        self._client = secretmanager.SecretManagerServiceClient()

    def create_secret(self, secret_id):
        parent = f"projects/{self._project_id}"
        secret = {'replication': {'automatic': {}}}
        response = self._client.create_secret(secret_id=secret_id, parent=parent, secret=secret)
        print(f'Created secret: {response.name}')

    def assign_secret(self, secret_id, payload):
        parent = f"projects/{self._project_id}/secrets/{secret_id}"
        payload = payload.encode('UTF-8')
        response = self._client.add_secret_version(parent=parent, payload={'data': payload})
        print(f'Added secret version: {response.name}')

    def get_secret(self, secret_id, version_id="latest"):
        name = f"projects/{self._project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self._client.access_secret_version(name=name)
        return response.payload.data.decode('UTF-8')


def secret_hash(secret_value):
    # return the sha224 hash of the secret value
    return hashlib.sha224(bytes(secret_value, "utf-8")).hexdigest()
