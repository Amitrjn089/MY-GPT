# Backend/logic/boundary.py

def is_owner_related(query: str) -> bool:
    forbidden = [
        "capital",
        "who is",
        "what is",
        "history",
        "weather",
        "define"
    ]

    q = query.lower()
    return not any(word in q for word in forbidden)
