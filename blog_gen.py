from typing import Annotated
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_community.llms import Ollama
from langchain.schema import HumanMessage
from youtube_transcript_api import YouTubeTranscriptApi
import re
from IPython.display import Image, display
import requests
import json
import os
from urllib.parse import urlparse, parse_qs

class YouTubeBlogState(TypedDict):
    video_url: str
    transcript: Annotated[str, "add_transcript"]
    summary: Annotated[str, "generate_summary"]
    blog_post: Annotated[str, "generate_blog"]



def extract_transcript(state: YouTubeBlogState) -> YouTubeBlogState:
    video_url= state["video_url"]
    try:
        # Extract Video ID from URL
        video_id = video_url.split("v=")[-1].split("&")[0]

        # Fetch transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Convert transcript list to text
        transcript_text = "\n".join([entry["text"] for entry in transcript])

        state["transcript"] = transcript_text

        return state

    except Exception as e:
        return f"Error: {str(e)}"


def summarize_transcript(state: YouTubeBlogState) -> YouTubeBlogState:
    transcript = state["transcript"]
    
    prompt = f"""
    Summarize the following YouTube transcript while maintaining key insights:

    {transcript}
    
    Keep it concise and structured.
    """
    summary = llm.invoke(prompt)
    # summary = llm([HumanMessage(content=prompt)]).content
    state["summary"] = summary
    return state

def generate_blog(state: YouTubeBlogState) -> YouTubeBlogState:
    summary = state["summary"]
    
    prompt = f"""
    Convert the following summarized transcript into a well-structured blog post:
    
    {summary}
    
    The blog should be engaging, informative, and well-structured with an introduction, key takeaways, and a conclusion. 
    Also if any code is explained, include in the final blog the code snippet and explain briefly the code as well.
    """
    
    blog_post = llm.invoke(prompt)
    # blog_post = llm([HumanMessage(content=prompt)]).content
    state["blog_post"] = blog_post
    return state

def human_review(state: YouTubeBlogState) -> YouTubeBlogState:
    print("\n--- Blog Review ---\n")
    print(state["blog_post"])  # Show blog to reviewer
    decision = input("\nApprove blog? (yes/no): ").strip().lower()
    
    if decision == "yes":
        state["review_approved"] = True
        state["human_feedback"] = ""  # No feedback needed
    else:
        state["review_approved"] = False
        state["human_feedback"] = input("\nProvide feedback for improvement: ")
    
    return state

def revise_blog(state: YouTubeBlogState) -> YouTubeBlogState:
    blog_post = state["blog_post"]
    feedback = state["human_feedback"]
    
    prompt = f"""
    Here is a blog post:

    {blog_post}

    The reviewer has given the following feedback:
    "{feedback}"

    Please improve the blog based on this feedback.
    """
    
    revised_blog = llm.invoke(prompt)
    state["blog_post"] = revised_blog
    return state

def should_continue(state: YouTubeBlogState):
    """ Return the next node to execute """

    # Check if approved:
    
    if state["review_approved"]:
        return END
    
    # Otherwise 
    return "revise_blog"

llm = Ollama(model="llama3.2:1b")
workflow = StateGraph(YouTubeBlogState)

# Define nodes
workflow.add_node("extract_transcript", extract_transcript)
workflow.add_node("summarize_transcript", summarize_transcript)
workflow.add_node("generate_blog", generate_blog)
workflow.add_node("human_review", human_review)
workflow.add_node("revise_blog", revise_blog)

# Define execution order
workflow.add_edge(START, "extract_transcript")
workflow.add_edge("extract_transcript", "summarize_transcript")
workflow.add_edge("summarize_transcript", "generate_blog")
workflow.add_edge("generate_blog", "human_review")

# Conditional feedback loop: If rejected, revise the blog and review again
workflow.add_conditional_edges(
    "human_review", should_continue, ["revise_blog", END]
)
workflow.add_edge("revise_blog", "human_review")  # Retry loop

# Compile the workflow
executor = workflow.compile()





