import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from zai_integration import get_chat_completion

def run_example():
    """
    Runs an example of getting a chat completion from the Z.AI API.
    """
    print("Getting chat completion from Z.AI...")
    prompt = "Hello, Z.AI! Tell me a joke about AI."
    try:
        response = get_chat_completion(prompt)
        print(f"Prompt: {prompt}")
        print(f"Response: {response}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    run_example()
