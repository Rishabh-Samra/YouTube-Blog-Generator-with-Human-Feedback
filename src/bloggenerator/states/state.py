from typing import Annotated, TypedDict
from typing_extensions import TypedDict
# from langchain_core.messages import HumanMessage, AIMessage

class YouTubeBlogState(TypedDict):
    video_url: str
    transcript: Annotated[str, "add_transcript"]
    summary: Annotated[str, "generate_summary"]
    blog_post: Annotated[str, "generate_blog"]