from src.bloggenerator.states.state import YouTubeBlogState
from youtube_transcript_api import YouTubeTranscriptApi

class ExtractTranscript:
    """
    Extracts the transcript
    """
    def __init__(self):
        pass

    def process(self, state: YouTubeBlogState) -> dict:
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