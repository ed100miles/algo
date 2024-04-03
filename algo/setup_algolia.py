from sys import getsizeof
from time import sleep
from typing import List
from os import getenv
import json

from algoliasearch.search_client import SearchClient
from algoliasearch.exceptions import AlgoliaUnreachableHostException
from dotenv import load_dotenv, find_dotenv
import bw2data as bd


load_dotenv(find_dotenv())

ALGOLIA_APP_ID = getenv("ALGOLIA_APP_ID")
ALGOLIA_API_KEY = getenv("ALGOLIA_API_KEY")
ALGOLIA_INDEX_NAME = getenv("ALGOLIA_INDEX_NAME", "test_index")


def get_algolia_index():
    # Connect and authenticate with your Algolia app
    client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
    # Create a new index and add a record
    index = client.init_index(ALGOLIA_INDEX_NAME)
    return index


def add_bw_data_to_algolia():
    bd.projects.set_current("base_project")
    db = list(bd.Database("ei_391"))
    BATCH_SIZE = 1_000
    batch = 0
    index = get_algolia_index()
    while batch < len(db):
        retries = 3
        print(f"Processing batch: {batch} - {batch + BATCH_SIZE}")
        """
        The getsizeof part below checks that the record is not too large for algolia,
        if it is, we filter it out for now"""
        records: List[dict] = [
            {**act.as_dict(), "objectID": act.as_dict()["code"]}
            for act in db[batch : batch + BATCH_SIZE]
            if getsizeof(json.dumps(act.as_dict())) < 10000
        ]
        while retries > 0:
            try:
                index.save_objects(records)
                break
            except AlgoliaUnreachableHostException as e:
                index = get_algolia_index()  # Reconnect to Algolia
                print(f"Error: {e}")
                retries -= 1
                if retries == 0:
                    print(
                        f"Failed to add batch {batch} - {batch + BATCH_SIZE} to Algolia"
                    )
                    raise e
                sleep(30)
        batch += BATCH_SIZE


def delete_all_records():
    index = get_algolia_index()
    index.clear_objects()


if __name__ == "__main__":
    """
    # delete_all_records()
    # add_bw_data_to_algolia()
    """
    pass
