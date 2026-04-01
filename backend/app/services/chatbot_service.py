from sqlalchemy.orm import Session
from app.models.category import Category
from app.models.issue import Issue
from app.utils.gemini_client import ask_gemini


# -----------------------------
# Intent Detection (Simple Rule-Based)
# -----------------------------
def detect_intent(message: str):
    message = message.lower()

    if "categories" in message or "category" in message:
        return "GET_CATEGORIES"

    if "my issues" in message or "my complaints" in message:
        return "GET_MY_ISSUES"

    return "GENERAL"


# -----------------------------
# Smart Chat Handler
# -----------------------------
def handle_chat(message: str, db: Session, user):

    intent = detect_intent(message)
    print(f"Detected intent: {intent}")
    # -----------------------------
    # Case 1: Get Categories
    # -----------------------------
    if intent == "GET_CATEGORIES":
        categories = db.query(Category).filter(
            Category.college_id == user.college_id
        ).all()

        if not categories:
            return "No categories available for your college."

        category_list = [c.name for c in categories]

        return f"Available categories: {', '.join(category_list)}"


    # -----------------------------
    # Case 2: Get User Issues
    # -----------------------------
    if intent == "GET_MY_ISSUES":
        issues = db.query(Issue).filter(
            Issue.user_id == user.id
        ).all()

        if not issues:
            return "You have not reported any issues yet."

        response = []
        for issue in issues:
            response.append(f"{issue.title} - {issue.status}")

        return "\n".join(response)


    # -----------------------------
    # Case 3: General AI Response
    # -----------------------------
    return ask_gemini(message)