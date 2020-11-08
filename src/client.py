from typing import Dict

import streamlit as st
import streamlit.components.v1 as components

from dataset import extract_section_to_urls
from dataset import load_topics


@st.cache
def load_data(path_to_folder: str) -> Dict[str, Dict[str, str]]:
    """Load data as section -> mapping of urls to their titles"""
    all_topics = load_topics(path_to_folder)
    section_to_urls = {
        section: {link.url: link.title for link in links}
        for section, links in extract_section_to_urls(all_topics).items()
    }
    return section_to_urls


def main():
    st.title("Streamlit Weekly Roundups Explorer")
    st.sidebar.subheader("Configuration")
    section_to_urls = load_data("./data")

    selected_section = st.sidebar.selectbox(
        "Select section: ", sorted(section_to_urls.keys())
    )
    urls_to_title = section_to_urls[selected_section]

    selected_url = st.selectbox(
        "Search for a link:",
        list(urls_to_title.keys()),
        format_func=lambda option: urls_to_title[option],
    )
    st.markdown(f"URL: {selected_url}")
    st.markdown("Embedded page below. If it does not work, click on the URL above")
    components.iframe(selected_url, height=1200, scrolling=True)


if __name__ == "__main__":
    main()
