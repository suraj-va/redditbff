from typing import List, Optional
import numpy as np

from .post import Post

from summarizer import summarize_cluster

class Cluster:
    def __init__(self, posts: List[Post]):
        self.posts = posts
        self.mean = np.zeros(posts[0].embedding.shape)
        for post in posts:
            self.mean += post.embedding
        self.mean /= len(posts)
        self.summary = None

    def merge(self, cluster):
        self.mean = (
            len(self.posts) * self.mean + len(cluster.posts) * cluster.mean
        ) / (len(self.posts) + len(cluster.posts))
        self.posts += cluster.posts

    def summarize(self):
        if self.summary is None:
            self.summary = summarize_cluster(self.posts)
        return self.summary
