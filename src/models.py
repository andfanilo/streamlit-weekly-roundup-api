from typing import List
from typing import Optional

from pydantic import AnyHttpUrl
from pydantic import BaseModel
from pydantic import Field
from pydantic import validator

########################################################################
# Models for parsing JSON data
########################################################################


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


########################################################################
# Models for FastAPI
########################################################################


class StatusResponse(BaseModel):
    message: str = Field(..., example="Hello world")


class Section(BaseModel):
    id: int
    name: str
    slug: str

    @validator("slug")
    def name_and_slug_match(cls, v, values):
        if v != values["name"].lower().replace(" ", "-"):
            raise ValueError("slug and name do not match")
        return v

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Streamlit Updates",
                "slug": "streamlit-updates",
            }
        }


class ListSections(BaseModel):
    sections: List[Section]
