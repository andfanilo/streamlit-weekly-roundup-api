import streamlit as st
import streamlit.components.v1 as components

from dataset import extract_urls
from dataset import load_topics


def main():
    st.title("Parsing Streamlit Weekly Roundups")
    all_topics = load_topics("./data")
    urls_to_title = extract_urls(all_topics)

    selected_url = st.selectbox(
        "Search for a link:",
        list(urls_to_title.keys()),
        format_func=lambda option: urls_to_title[option],
    )
    st.markdown(f"URL: {selected_url}")
    components.iframe(selected_url, height=1200, scrolling=True)


if __name__ == "__main__":
    main()
