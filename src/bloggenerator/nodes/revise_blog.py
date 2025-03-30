from src.bloggenerator.states.state import YouTubeBlogState


class ReviseBlog:
    """
    Revise Blog
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state: YouTubeBlogState) -> dict:
        blog_post = state["blog_post"]
        feedback = state["human_feedback"]
        
        prompt = f"""
        Here is a blog post:

        {blog_post}

        The reviewer has given the following feedback:
        "{feedback}"

        Please improve the blog based on this feedback.
        """
        
        revised_blog = self.llm.invoke(prompt)
        state["blog_post"] = revised_blog
        return state