import logging
import json
from pathlib import Path

import requests
import typer


def main():
    typer.echo("Start scraping")

    all_topics_resp = requests.get(
        "https://discuss.streamlit.io/tag/weekly-roundup.json"
    )
    assert all_topics_resp.status_code == 200
    all_topics = all_topics_resp.json()["topic_list"]["topics"]
    logging.info(
        f"Fetched all topics under weekly roundup tag: got {len(all_topics)} topics"
    )

    latest_topic_id, latest_topic_slug = sorted(
        [(int(topic["id"]), topic["slug"]) for topic in all_topics],
        key=lambda tup: tup[0],
        reverse=True,
    )[0]

    logging.info(f"Checking if topic {latest_topic_id} already downloaded...")
    if Path(f"./data/{latest_topic_id}.json").is_file():
        logging.info(f"Topic {latest_topic_id} already downloaded, exiting...")
        return

    latest_topic_url = (
        f"https://discuss.streamlit.io/t/{latest_topic_slug}/{latest_topic_id}.json"
    )
    logging.info(f"Fetch URL {latest_topic_url}")
    latest_topic_resp = requests.get(latest_topic_url)
    assert latest_topic_resp.status_code == 200

    file_contents = latest_topic_resp.json()
    with open(f"./data/{latest_topic_id}.json", "w") as out_file:
        json.dump(file_contents, out_file)
        logging.info(f"URL contents written to './data/{latest_topic_id}.json'")

    typer.echo("End scraping")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    typer.run(main)
