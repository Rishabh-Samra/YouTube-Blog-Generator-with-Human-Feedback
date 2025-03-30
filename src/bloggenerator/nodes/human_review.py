from src.bloggenerator.states.state import YouTubeBlogState


class HumanReview:
    """
    Human review
    """
    def __init__(self):
        pass

    def process(state: YouTubeBlogState) -> YouTubeBlogState:
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