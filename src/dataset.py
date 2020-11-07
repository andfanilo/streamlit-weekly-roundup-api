import itertools

from pathlib import Path
from typing import Dict
from typing import List
from typing import Optional

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


def load_topics(path_to_folder: str) -> List[Topic]:
    all_files = Path(path_to_folder).rglob("*.json")
    parsed_files = [Topic.parse_file(file) for file in all_files]
    return parsed_files


def extract_urls(topics: List[Topic]) -> Dict[str, str]:
    all_links = itertools.chain.from_iterable(
        [topic.details.links for topic in topics]
    )
    return {l.url: l.title for l in all_links if l.title is not None}
