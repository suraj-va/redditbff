import numpy as np

class Post:
    def __init__(
        self,
        id: str,
        title: str,
        content: str,
        url: str,
        score: int,
        upvote_ratio: float,
        num_comments: int,
        created: int,
        embedding: np.ndarray,
    ):
        self.id = id
        self.title = title
        self.content = content
        self.url = url
        self.score = score
        self.upvote_ratio = upvote_ratio
        self.num_comments = num_comments
        self.created = created
        self.embedding = embedding