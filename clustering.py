import numpy as np
from sklearn.manifold import TSNE
from typing import List
from data.cluster import Cluster
from data.post import Post


def agglomerative_cluster(posts: List[Post], dist_thresh=0.77):
    """keep clustering until dist_thresh is met"""
    clusters = [Cluster([post]) for post in posts]
    should_continue = True
    while should_continue:
        c1 = None
        c1_idx = None
        c2 = None
        c2_idx = None
        sim = None
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                ci = clusters[i]
                cj = clusters[j]
                sij = ci.mean.dot(cj.mean)
                if sim is None or sij > sim:
                    c1 = ci
                    c2 = cj
                    c1_idx = i
                    c2_idx = j
                    sim = sij

        if c1 and sim >= dist_thresh:
            c1.merge(c2)
            new_clusters = []
            for k in range(len(clusters)):
                if k != c1_idx and k != c2_idx:
                    new_clusters.append(clusters[k])
            new_clusters.append(c1)
            clusters = new_clusters
        else:
            break

    return clusters


def assign_tsne_coordinates(posts: List[Post]):
    """assign tsne coordinates to posts"""
    X = np.array([p.embedding for p in posts])
    X_tsne = TSNE(
        n_components=2, learning_rate="auto", init="random", perplexity=3
    ).fit_transform(X)
    max_abs_x = max([abs(coords[0]) for coords in X_tsne])
    max_abs_y = max([abs(coords[1]) for coords in X_tsne])
    for i, coords in enumerate(X_tsne):
        posts[i].xy = [coords[0] / max_abs_x, coords[1] / max_abs_y]
