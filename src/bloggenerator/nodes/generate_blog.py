from src.bloggenerator.states.state import YouTubeBlogState
import streamlit as st

class GenerateBlog:
    """
    Generate the blog
    """
    
    def __init__(self, model):
        self.llm = model

    def process(self, state: YouTubeBlogState) -> dict:
        summary = state["summary"]
    
        prompt = f"""
        Convert the following summarized transcript into a well-structured blog post:
        
        {summary}
        
        The blog should be engaging, informative, and well-structured with an introduction, key takeaways, and a conclusion. 
        Also if any code is explained, include in the final blog the code snippet and explain briefly the code as well.
        """
        
        blog_post = self.llm.invoke(prompt)
        state["blog_post"] = blog_post
        # Display the generated blog post in Markdown.
        blog_post = state.get("blog_post", "")
        st.markdown("### Generated Blog Post")
        st.markdown(blog_post, unsafe_allow_html=True)

        return state