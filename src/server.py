import itertools

from typing import Optional
from typing import List

from dataset import extract_section_to_urls
from dataset import load_topics
from fastapi import FastAPI
from fastapi import Query
from models import Link, LinksResponse
from models import Section
from models import SectionsResponse
from models import StatusResponse


app = FastAPI(title="Streamlit Weekly Roundup API")
all_topics = load_topics("../data")
section_to_urls = extract_section_to_urls(all_topics)
slug_to_section = {
    section.lower().replace(" ", "-"): section
    for section in sorted(section_to_urls.keys())
}


@app.get("/status", response_model=StatusResponse, response_description="API status")
def get_api_status():
    """Get API Status"""
    return {"message": "Hello World"}


@app.get(
    "/sections",
    response_model=SectionsResponse,
    response_description="List of sections",
)
def get_all_sections():
    """Get all sections"""
    return {
        "sections": [
            Section(id=ind, name=section, slug=slug)
            for ind, (slug, section) in enumerate(slug_to_section.items())
        ]
    }


@app.get(
    "/links",
    response_model=LinksResponse,
    response_description="List of paginated links",
)
def get_links(
    section_slug: Optional[str] = Query(
        None, description="Slug for section to filter on"
    ),
    page: int = 0,
    number_links: int = Query(50, description="Number of elements to return", le=500),
):
    """Get a set of paginated links"""
    urls: List[Link] = []
    if not section_slug:
        urls = list(itertools.chain.from_iterable(section_to_urls.values()))
    else:
        urls = section_to_urls[slug_to_section[section_slug]]
    total_number_links = len(urls)
    response = urls[page * number_links : (page + 1) * number_links]
    number_links_response = len(response)
    next_url = (
        f"/links?page={page + 1}&number_links={number_links}"
        if (page + 1) * number_links < total_number_links
        else None
    )
    return {"next_url": next_url, "length": number_links_response, "links": response}
