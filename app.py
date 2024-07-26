import copy
import praw
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
from scraper import get_clusters
from dataclasses import asdict

reddit = praw.Reddit(
    client_id="9XcDEBYujPAym53w9QSdfA",
    client_secret="-URyEXDk5ZnthGOq5jyD9MviBt2ZgA",
    password="Teamawsome123",
    user_agent="reddit bff scraper",
    username="Wide-Panic4270",
)

st.write(
    """
# RedditBff: Reddit Analysis Tool
 👋 *world!* Enter subreddits of interest to begin (comma separated).
"""
)

with st.form(key="analyze form"):
    text_input = st.text_input(label="Enter the subreddits")
    submit_button = st.form_submit_button(label="Analyze")

subreddits = text_input.split(",")

if len(subreddits) > 0 and subreddits[0] != "":
    if "clusters" not in st.session_state:
        st.session_state["clusters"] = get_clusters(reddit, subreddits)
    clusters = st.session_state["clusters"]
    chart_dfs = []
    for i, cluster in enumerate(clusters):
        xy = np.stack([p.xy for p in cluster.posts])
        df = pd.DataFrame(xy, columns=["x", "y"])
        df["cluster"] = cluster.title
        chart_dfs.append(copy.deepcopy(df))

    config = {
        "mark": {"type": "circle", "size": 60},
        "params": [{"name": "point_selection", "select": "point"},],
        "encoding": {
            "x": {"field": "x", "type": "quantitative"},
            "y": {"field": "y", "type": "quantitative"},
            "color": {"field": "cluster", "type": "nominal"},
        },
    }

    new_df = pd.concat(chart_dfs)
    c = st.vega_lite_chart(
        new_df, config, theme="streamlit", use_container_width=True, on_select="rerun"
    )

    selection = c.get("selection").get("point_selection")
    if selection and len(selection) > 0:
        selection_title = selection[0].get("cluster")
        chosen_cluster = None
        for cluster in clusters:
            if cluster.title == selection_title:
                chosen_cluster = cluster
                break

        # summarize the cluster
        chosen_cluster.summarize()

        # Get header and markdown
        st.header(f"⭐️ {chosen_cluster.title}")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"{chosen_cluster.summary}")

        with col2:
            st.subheader("Example Posts:")
            for post in chosen_cluster.posts[:3]:
                st.markdown(f"🔗 [{post.title}]({post.url})")

        # Get cluster stats
        stats = cluster.get_stats()
        stats_df = pd.DataFrame({k: [v] for k, v in asdict(stats).items()})
        st.subheader("📊 Cluster Stats")
        st.table(stats_df)

        if st.button("Cluster AGAIN!"):
            pass

        if st.button("How are people reacting?"):
            pass

        # Further query
        with st.form(key="query form"):
            query_input = st.text_input(label="Query this cluster...")
            query_button = st.form_submit_button(label="Query")

        if query_input and query_input != "":
            pass
    else:
        st.markdown("🔍 Click on a cluster to magnify...")

    # s = ""
    # for i in range(len(clusters)):
    #     s += "- " + f"{clusters[i].title}" + clusters[i].summary + "\n"
    # st.markdown(s)
