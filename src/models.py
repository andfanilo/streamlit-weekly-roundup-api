from typing import List
from typing import Optional

from pydantic import AnyHttpUrl
from pydantic import BaseModel
from pydantic import Field

########################################################################
# Models for parsing JSON data
########################################################################


class Link(BaseModel):
    url: AnyHttpUrl = Field(..., example="https://www.streamlit.io/sharing")
    title: Optional[str] = Field(None, example="Streamlit Sharing")


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


########################################################################
# Models for FastAPI
########################################################################


class StatusResponse(BaseModel):
    message: str = Field(..., example="Hello world")


class Section(BaseModel):
    id: int
    name: str
    slug: str

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Streamlit Updates",
                "slug": "streamlit-updates",
            }
        }


class SectionsResponse(BaseModel):
    sections: List[Section]


class LinksResponse(BaseModel):
    next_url: Optional[str] = Field(
        None,
        description="URL for next batch of links. If null, then there are no more links.",
        example="/links?page=4&number_links=50",
    )
    length: int = Field(..., example=50)
    links: List[Link]
