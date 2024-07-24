import streamlit as st

st.write(
    """
# RedditBff: Reddit Analysis Tool
 👋 *world!* Enter subreddits of interest to begin (comma separated).
"""
)

subreddits = st.text_area("Subreddits")
button = st.button("Analyze")
