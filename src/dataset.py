import logging

from functools import reduce
from pathlib import Path
from typing import Dict
from typing import List

from bs4 import BeautifulSoup
from models import Link
from models import Topic
from pydantic import ValidationError


def _merge_dict_of_lists(
    dict1: Dict[str, List], dict2: Dict[str, List]
) -> Dict[str, List]:
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = value + dict1[key]
    return dict3


def _validate_link(link: str) -> bool:
    """Validate URL using Pydantic's AnyHttpUrl's validator"""
    try:
        Link(url=link)
        return True
    except ValidationError:
        logging.warn(f"error parsing URL: {link}")
        return False


def load_topics(path_to_folder: str) -> List[Topic]:
    """Parse list of topics as JSON files from Discourse API"""
    all_files = Path(path_to_folder).rglob("*.json")
    parsed_files = [Topic.parse_file(file) for file in all_files]
    return parsed_files


def extract_section_to_urls(topics: List[Topic]) -> Dict[str, List[Link]]:
    """Create Dict of topic section to mapping of URL to titles, like:

    {
        "Streamlit Updates": [
            Link(url="https://www.streamlit.io/sharing", title="Streamlit sharing was announced today"),
            Link(url="https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/", title="Check out the new Streamlit Sharing")
        ],
        "Articles": [
            ...
        ],
        ...
    }
    """
    parsed_html_per_topic = [
        BeautifulSoup(topic.post_stream.posts[0].cooked, "html.parser")
        for topic in topics
    ]

    section_to_links_per_topic = [
        {
            h2_section.text.strip(): [
                Link(url=li.find("a")["href"], title=li.text.strip())
                for li in h2_section.find_next_sibling("ul").find_all("li")
                if li.find("a") is not None and _validate_link(li.find("a")["href"])
            ]
            for h2_section in topic_html.find_all("h2")
        }
        for topic_html in parsed_html_per_topic
    ]

    section_to_links = reduce(_merge_dict_of_lists, section_to_links_per_topic)

    return section_to_links
