import praw
import uuid
import numpy as np

from sentence_transformers import SentenceTransformer
from clustering import agglomerative_cluster, assign_tsne_coordinates

from data.cluster import Post


def get_clusters(reddit, subreddits):
    all_posts = []
    embedding_model = SentenceTransformer("thenlper/gte-base")
    # get subreddit posts
    for sub in subreddits:
        try:
            subreddit = reddit.subreddit(sub.split("/")[1])
        except:
            print(f"Subreddit {sub} not found.")
            continue
        # Fetch the latest posts (you can change the limit as needed)
        latest_posts = subreddit.new(limit=10)
        # Print the titles and URLs of the latest posts
        for post in latest_posts:
            post_embedding = embedding_model.encode(post.title + " \n " + post.selftext)
            post_embedding = post_embedding / np.linalg.norm(post_embedding)
            post_id = str(uuid.uuid4())
            p = Post(
                id=post_id,
                title=post.title,
                content=post.selftext,
                url=post.url,
                score=post.score,
                upvote_ratio=post.upvote_ratio,
                num_comments=post.num_comments,
                created=post.created,
                embedding=post_embedding,
                num_saved=post.saved,
            )
            all_posts.append(p)

    # get tsne coordinates
    assign_tsne_coordinates(all_posts)
    # cluster posts
    clusters = agglomerative_cluster(all_posts)
    for cl in clusters:
        summ = cl.get_title()
    return clusters
