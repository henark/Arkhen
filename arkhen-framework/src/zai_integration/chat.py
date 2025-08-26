from .client import get_zai_client

def get_chat_completion(prompt: str, model: str = "glm-4.5") -> str:
    """
    Gets a chat completion from a Z.AI model.

    Args:
        prompt (str): The prompt to send to the model.
        model (str, optional): The model to use. Defaults to "glm-4.5".

    Returns:
        str: The content of the model's response.
    """
    client = get_zai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
