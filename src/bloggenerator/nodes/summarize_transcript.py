from src.bloggenerator.states.state import YouTubeBlogState


class SumarizeTranscript:
    """
    Summarize the transcript
    """
    
    def __init__(self, model):
        self.llm = model

    def process(self, state: YouTubeBlogState) -> dict:
        transcript = state["transcript"]
    
        prompt = f"""
        Summarize the following YouTube transcript while maintaining key insights:

        {transcript}
        
        Keep it concise and structured.
        """

        summary = self.llm.invoke(prompt)
        state["summary"] = summary
        return state