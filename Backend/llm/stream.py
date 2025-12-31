from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def stream_response(system_prompt: str, context: list[str], query: str):
    """
    Synchronous generator that yields tokens one by one.
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "system",
            "content": "Context:\n" + "\n".join(context)
        },
        {"role": "user", "content": query}
    ]

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content
