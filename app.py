import streamlit as st
from blog_gen import (
    YouTubeBlogState,
    extract_transcript,
    summarize_transcript,
    generate_blog,
    revise_blog,
    llm  # the Ollama LLM instance from your script
)

st.title("📹 YouTube Blog Generator with Human-in-the-Loop")

# Input: Ask user for YouTube video link.
video_url = st.text_input("Enter YouTube Video URL:")

if video_url:
    st.info("Processing video... please wait.")
    
    # Create the initial state.
    # Note: Our YouTubeBlogState requires at least "video_url".
    state: YouTubeBlogState = {"video_url": video_url}
    
    # Run the workflow steps (excluding human_review, which we replace with a Streamlit UI)
    try:
        state = extract_transcript(state)
        state = summarize_transcript(state)
        state = generate_blog(state)
    except Exception as e:
        st.error(f"An error occurred during processing: {e}")
    
    # Display the generated blog post in Markdown.
    blog_post = state.get("blog_post", "")
    st.markdown("### Generated Blog Post")
    st.markdown(blog_post, unsafe_allow_html=True)
    
    # Ask for human review via the UI.
    st.markdown("### Human Review")
    approval = st.radio("Do you approve the blog post?", ("Yes", "No"))
    
    if approval == "Yes":
        st.success("Blog post approved!")
        st.markdown("### Final Blog Post")
        st.markdown(blog_post, unsafe_allow_html=True)
    else:
        feedback = st.text_area("Please provide your feedback for improvement:")
        if st.button("Revise Blog"):
            # Update state with the human feedback.
            state["review_approved"] = False
            state["human_feedback"] = feedback
            
            # Revise the blog post using the provided feedback.
            state = revise_blog(state)
            revised_blog = state.get("blog_post", "")
            st.markdown("### Revised Blog Post")
            st.markdown(revised_blog, unsafe_allow_html=True)
            
            # Optionally, let the user decide again.
            st.info("If you are still not satisfied, you can provide further feedback and click 'Revise Blog' again.")

