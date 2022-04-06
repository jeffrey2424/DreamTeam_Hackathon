import os
from argparse import ArgumentParser

import pandas as pd
import numpy as np
import requests
from google.cloud import storage


def load_single_logo(client, bucket_name, url, image_name):
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(image_name)

    req = requests.get(url, stream=True)
    blob.upload_from_string(req.content)


def get_image_name(company_code):
    return company_code + ".png"


def load_all_images(client, bucket_name, input_filename):
    df = pd.read_csv(input_filename)

    # Fuck you all, I'll iterate over a DataFrame if I want!!!
    for index, row in df.iterrows():
        if row["image_url"] is not np.nan:
            image_name = get_image_name(row["Code"])
            load_single_logo(
                client=client,
                bucket_name=bucket_name,
                url=row["image_url"],
                image_name=image_name
            )
            print(f"Loaded {row['Name']}")
        else:
            print(f"Skipping for {row['Name']}")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_filename", default="../data/company_name_mappings_mid.csv")
    parser.add_argument("--bucket_name", default="hackathon-team-10-company-logos")
    args = parser.parse_args()

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("Please input the path to your GOOGLE_APPLICATION_CREDENTIALS")
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = input("Path:")

    client = storage.Client()

    load_all_images(
        client=client,
        bucket_name=args.bucket_name,
        input_filename=args.input_filename,
    )
