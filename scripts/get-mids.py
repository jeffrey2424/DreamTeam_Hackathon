""" Get MIDs (Google identity IDs) for companies in the list. """
import os
import json
import subprocess
from contextlib import suppress
from multiprocessing.pool import ThreadPool
import urllib.parse
import pandas as pd
from argparse import ArgumentParser

# TODO: Also query with ticker?


def submit_query(query, api_key):

    parsed_query = urllib.parse.quote(query)

    # Build command
    cmd = "curl "
    cmd += "'https://kgsearch.googleapis.com/v1/entities:search?"
    cmd += f"query={parsed_query}"
    cmd += "&types=Organization"
    cmd += f"&key={api_key}'"
    cmd += " --header 'Accept: application/json'"
    cmd += " --compressed"

    print(cmd)

    # Submit query and get result
    result = subprocess.check_output(cmd, shell=True)

    return result


def build_query(series) -> str:
    """
    """
    name = series["Name"]

    return name


def parse_response(response):
    """
    """
    json_data = json.loads(response)

    entity_md = json_data["itemListElement"][0]["result"]

    return entity_md


def process_row(series):
    """
    """
    query = build_query(series)
    response = submit_query(query, api_key=api_key)

    try:
        parsed_response = parse_response(response)

        updated_row = series.copy()
        for k, v in parsed_response.items():
            if k.startswith("@"):
                k = k[1:]
            updated_row[k] = v

        # Add MID column
        mid = updated_row["id"]
        if mid.startswith("kg:"):
            mid = mid[3:]
        updated_row["mid"] = mid

        # Add image URL
        # NOTE: Sometimes response does not contain image
        with suppress(KeyError):
            updated_row["image_url"] = updated_row["image"]["contentUrl"]

        # Cleanup columns
        updated_row["name"] = "gkg_name"

        for k in ("type", "image", "description"):
            with suppress(KeyError):
                del updated_row[k]
        with suppress(KeyError):
            del updated_row["detailedDescription"]

    except Exception as err:
        print(f"Failed to get MID for {series['Name']}: {err}")
        print(response.decode())
        updated_row = series.copy()

    return updated_row


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("--input_filename", default="data/test_data/companies.csv")
    parser.add_argument("--output_filename", default="data/test_data/companies_mid.csv")
    args = parser.parse_args()

    api_key = os.environ["API_KEY"]

    df = pd.read_csv(args.input_filename)

    with ThreadPool(4) as pool:
        output = pool.map(process_row, [df.iloc[i] for i in range(df.shape[0])])

    df_out = pd.concat(output, axis=1).T
    df_out.to_csv(args.output_filename, index=False)
