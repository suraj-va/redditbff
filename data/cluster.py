from dataclasses import dataclass
from typing import List, Optional
from statistics import mean as average
import numpy as np

from .post import Post

from summarizer import summarize_cluster, get_title


@dataclass
class ClusterStats:
    """Class for cluster stats"""

    num_total_posts: int
    avg_upvote_ratio: float
    avg_num_comments: float
    avg_num_saved: float


class Cluster:
    def __init__(self, posts: List[Post]):
        self.posts = posts
        self.mean = np.zeros(posts[0].embedding.shape)
        for post in posts:
            self.mean += post.embedding
        self.mean /= len(posts)
        self.summary = None
        self.title = None

    def merge(self, cluster):
        self.mean = (
            len(self.posts) * self.mean + len(cluster.posts) * cluster.mean
        ) / (len(self.posts) + len(cluster.posts))
        self.posts += cluster.posts

    def get_title(self):
        if self.title is None:
            self.title = get_title(self.posts)
        return self.title

    def summarize(self):
        if self.summary is None:
            self.summary = summarize_cluster(self.posts)
        return self.summary

    def get_stats(self):
        return ClusterStats(
            num_total_posts=len(self.posts),
            avg_upvote_ratio=average([p.upvote_ratio for p in self.posts]),
            avg_num_comments=average([p.num_comments for p in self.posts]),
            avg_num_saved=average([p.num_saved for p in self.posts]),
        )
