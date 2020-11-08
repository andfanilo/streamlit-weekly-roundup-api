from dataset import extract_section_to_urls
from dataset import load_topics
from fastapi import FastAPI
from models import ListSections
from models import Section
from models import StatusResponse


app = FastAPI(title="Streamlit Weekly Roundup API")
all_topics = load_topics("../data")
section_to_urls = extract_section_to_urls(all_topics)
slug_to_section = {
    section.lower().replace(" ", "-"): section
    for section in sorted(section_to_urls.keys())
}


@app.get("/status", response_model=StatusResponse)
def get_api_status():
    return {"message": "Hello World"}


@app.get("/sections", response_model=ListSections)
def get_all_sections():
    return {
        "sections": [
            Section(id=ind, name=section, slug=slug)
            for ind, (slug, section) in enumerate(slug_to_section.items())
        ]
    }
