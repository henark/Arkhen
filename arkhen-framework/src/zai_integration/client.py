import os
from zai import ZaiClient
from dotenv import load_dotenv

def get_zai_client() -> ZaiClient:
    """
    Initializes and returns a ZaiClient.

    This function loads the environment variables from a .env file,
    retrieves the ZAI_API_KEY, and uses it to create a ZaiClient instance.

    Returns:
        ZaiClient: An instance of the ZaiClient.

    Raises:
        ValueError: If the ZAI_API_KEY is not found in the environment variables.
    """
    load_dotenv()
    api_key = os.getenv("ZAI_API_KEY")
    if not api_key:
        raise ValueError("ZAI_API_KEY not found in environment variables.")

    return ZaiClient(api_key=api_key)
