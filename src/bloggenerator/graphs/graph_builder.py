from langgraph.graph import StateGraph, START,END, MessagesState
from langgraph.prebuilt import tools_condition,ToolNode
from langchain_core.prompts import ChatPromptTemplate
from src.bloggenerator.states.state import YouTubeBlogState
from src.bloggenerator.nodes.extract_transcript import ExtractTranscript
from src.bloggenerator.nodes.summarize_transcript import SumarizeTranscript
from src.bloggenerator.nodes.generate_blog import GenerateBlog
from src.bloggenerator.nodes.human_review import HumanReview
from src.bloggenerator.nodes.revise_blog import ReviseBlog
import streamlit as st

class GraphBuilder:
    def __init__(self,model):
        self.llm=model
        self.graph_builder=StateGraph(YouTubeBlogState)
    
    def should_continue(state: YouTubeBlogState):
        """ Return the next node to execute """

        # Check if approved:
        
        if state["review_approved"]:
            return END
        
        # Otherwise 
        return "revise_blog"

    def build_graph(self):
        self.extract_transcript_node = ExtractTranscript()
        self.graph_builder.add_node("extract_transcript", self.extract_transcript_node.process)

        self.summarize_transcript_node = SumarizeTranscript(self.llm)
        self.graph_builder.add_node("summarize_transcript", self.summarize_transcript_node.process)

        self.generate_blog_node = GenerateBlog(self.llm)
        self.graph_builder.add_node("generate_blog", self.generate_blog_node.process)

        self.human_review_node = HumanReview()
        self.graph_builder.add_node("human_review", self.human_review_node.process)

        self.revise_blog_node = ReviseBlog(self.llm)
        self.graph_builder.add_node("revise_blog", self.revise_blog_node.process)

        #edges
        self.graph_builder.add_edge(START, "extract_transcript")
        self.graph_builder.add_edge("extract_transcript", "summarize_transcript")
        self.graph_builder.add_edge("summarize_transcript", "generate_blog")
        self.graph_builder.add_edge("generate_blog", "human_review")
        # Conditional feedback loop: If rejected, revise the blog and review again
        self.graph_builder.add_conditional_edges(
            "human_review", self.should_continue, ["revise_blog", END]
        )
        self.graph_builder.add_edge("revise_blog", "human_review")

        return self.graph_builder.compile()

        
    




    

