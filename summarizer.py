from typing import List

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from secrets import OPENAI_API_KEY
from data.cluster import Post

llm = ChatOpenAI(model="gpt-4o", openai_api_key=OPENAI_API_KEY, temperature=0.1)

def summarize_cluster(posts: List[Post]):
    cluster_description_prompt_template = """
        Your job is to look through the following reddit posts and
        determine commanalities between them. Come up with a short
        two to three sentence summary that answers questions such as:
            - what are these posts generally about?
            - are users complaining about something (any particular pain points or challenges that they face)?
            - If they do mention any challenges, what are they doing currently to solve them?
            - are they mentioning the use of some software tools/websites?
            - do they mention any paid tools or services that they use to solve any problems they face?

        Here are the contents of the posts:

        {POSTS}

        Summary:
    """
    cluster_description_prompt = PromptTemplate.from_template(
        cluster_description_prompt_template
    )
    chain = cluster_description_prompt | llm
    res = chain.invoke({"POSTS": "\n ----- \n".join([post.content for post in posts])})
    return res.content
