
from rag.retrieve import retrieve_context


def search_personal_notes(query: str) -> dict:
    """
    Server-side tool:
    Search owner's personal notes via RAG.
    """
    results = retrieve_context(query)

    return {
        "type": "search_personal_notes",
        "results": results
    }


TOOLS = {
    "search_personal_notes": search_personal_notes
}
