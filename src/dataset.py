from functools import reduce

from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

from bs4 import BeautifulSoup
from pydantic import AnyHttpUrl
from pydantic import BaseModel


class Link(BaseModel):
    url: AnyHttpUrl
    title: Optional[str]
    domain: str
    root_domain: str


class Post(BaseModel):
    cooked: str
    link_counts: Optional[List]


class Details(BaseModel):
    links: List[Link]


class PostStream(BaseModel):
    posts: List[Post]


class Topic(BaseModel):
    title: str
    post_stream: PostStream
    details: Details


def _merge_dict_of_dicts(
    dict1: Dict[str, Dict], dict2: Dict[str, Dict]
) -> Dict[str, Dict]:
    dict3 = {**dict1, **dict2}
    for key, value in dict3.items():
        if key in dict1 and key in dict2:
            dict3[key] = {**value, **dict1[key]}
    return dict3


def load_topics(path_to_folder: str) -> List[Topic]:
    """Parse list of topics as JSON files from Discourse API"""
    all_files = Path(path_to_folder).rglob("*.json")
    parsed_files = [Topic.parse_file(file) for file in all_files]
    return parsed_files


def extract_section_to_urls(topics: List[Topic]) -> Dict[str, Dict]:
    """Create Dict of topic section to mapping of URL to titles, like:

    {
        "Streamlit Updates": {
            "https://www.streamlit.io/sharing":"Streamlit sharing was announced today",
            "https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/":"Check out the new Streamlit Sharing"
        },
        "Articles": {
            ...
        },
        ...
    }
    """
    parsed_html_per_topic = [
        BeautifulSoup(topic.post_stream.posts[0].cooked, "html.parser")
        for topic in topics
    ]

    section_to_links_per_topic = [
        {
            h2_section.text.strip(): {
                li.find("a")["href"]: li.text.strip()
                for li in h2_section.find_next_sibling("ul").find_all("li")
                if li.find("a") is not None
            }
            for h2_section in topic_html.find_all("h2")
        }
        for topic_html in parsed_html_per_topic
    ]

    section_to_links = reduce(_merge_dict_of_dicts, section_to_links_per_topic)

    return section_to_links
