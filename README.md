# YouTube Blog Generator with Human Feedback

This project automates the generation of a structured blog post from a **YouTube video transcript** using **LangGraph**, **LangChain**, and **Streamlit**. It incorporates **human-in-the-loop feedback**, allowing users to **approve or refine** the blog before finalizing it.

## 🚀 Features

- **Transcript Extraction:** Automatically retrieves the best available transcript from a given YouTube video.
- **LLM-Powered Blog Generation:** Uses the Ollama LLaMA 3.2 model to summarize and convert the transcript into a well-structured blog post.
- **Human Feedback Loop:** Allows users to review the generated blog, approve it, or provide feedback for iterative improvements.
- **Streamlit UI:** A user-friendly web interface to input the YouTube URL and interact with the review process.

## 📂 Project Structure

```
youtube-blog-generator/
├── blog_gen.py         # Core LangGraph workflow for generating blogs
├── app.py              # Streamlit web app for user input and feedback
├── requirements.txt    # List of required dependencies
└── README.md           # This file
```

## 🔧 Setup Instructions

### 1. Install Dependencies
Make sure you have **Python 3.8+** installed. Then, install the required packages using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit App
Launch the web interface with:

```bash
streamlit run app.py
```

This command will open a browser window where you can enter a YouTube link and generate a blog post.

## 🛠 How It Works

1. **Input YouTube URL:** The user provides a YouTube video link.
2. **Transcript Extraction:** 
   - The script extracts the video ID from the URL and fetches the best available transcript (prioritizing manually uploaded transcripts over auto-generated ones).
3. **Blog Generation:** 
   - The transcript is summarized and then transformed into a structured blog post using the LLM.
4. **Human Review:** 
   - The generated blog post is displayed for review. The user can either approve the blog or provide feedback.
5. **Iterative Refinement:** 
   - If feedback is provided, the blog is revised based on that feedback and the revised version is displayed again.

## 📦 Dependencies

The project relies on the following packages (as listed in `requirements.txt`):

```
streamlit
python-dotenv
youtube_transcript_api
langchain
langchain-groq
langchain-community
langgraph
langgraph-cli[inmem]
google-auth
google-auth-oauthlib
```

## 📌 Future Enhancements

- **Multi-language Support:** Improve transcript extraction to support additional languages such as Hindi, with automatic translation if necessary.
- **Enhanced Transcription:** Consider integrating Whisper AI for improved transcript accuracy.
- **Extended Review Features:** Implement multi-reviewer support and richer feedback mechanisms.

## 🤝 Contributing

Contributions are welcome! Please submit pull requests or open issues if you have suggestions or improvements.

---

Now you can generate high-quality blogs from YouTube videos with AI and human collaboration!
