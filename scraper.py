import praw
import uuid

from sentence_transformers import SentenceTransformer
from clustering import agglomerative_cluster

from data.cluster import Post


# def _convert_uuid_to_float_arr(uuid_str):
#     return np.array([float(ord(c)) for c in str(uuid_str)])


# def _convert_float_arr_to_uuid(float_arr):
#     return "".join([chr(int(c)) for c in float_arr])


subreddits = ["r/leetcode", "r/ADHD_Programmers"]

reddit = praw.Reddit(
    client_id="9XcDEBYujPAym53w9QSdfA",
    client_secret="-URyEXDk5ZnthGOq5jyD9MviBt2ZgA",
    password="Teamawsome123",
    user_agent="reddit bff scraper",
    username="Wide-Panic4270",
)

all_posts = []
embedding_model = SentenceTransformer("thenlper/gte-base")

# get subreddit posts
for sub in subreddits:
    try:
        subreddit = reddit.subreddit(sub.split("/")[1])
    except:
        print(f"Subreddit {subreddit} not found.")
        continue
    # Fetch the latest posts (you can change the limit as needed)
    latest_posts = subreddit.new(limit=10)
    # Print the titles and URLs of the latest posts
    for post in latest_posts:
        post_embedding = embedding_model.encode(post.title + " \n " + post.selftext)
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
        )
        all_posts.append(p)

# cluster posts
clusters = agglomerative_cluster(all_posts)

# display
print(f"Got a total of {len(clusters)} clusters. Here are the summaries...")

for cl in clusters:
    summ = cl.summarize()
    print(summ)
    print("\n****\n")
