import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from current directory .env and override existing ones
load_dotenv(".env", override=True)


def build_system_prompt():
    """Build basic system prompt."""
    return """You are an AI assistant. When responding to users, you should:
1. Provide helpful responses
2. Be direct and clear
3. Be confident about what you know and express uncertainty about what you don't"""


def generate_raw_response(user_message, verbose=False):
    """Generate a raw response without any principles or critique.

    Args:
        user_message: The message to respond to
        verbose: Whether to print intermediate steps (default: False)
    """
    system_prompt = build_system_prompt()

    # Print system prompt if verbose is True
    if verbose:
        print("=" * 80)
        print("SYSTEM PROMPT:")
        print("=" * 80)
        print(system_prompt)
        print("=" * 80)
        print()

    # Explicitly get the API key from the .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env file")

    # Get the model from environment variable
    model = os.getenv("OPENAI_MODEL")
    if not model:
        raise ValueError("OPENAI_MODEL not found in .env file")

    # Get temperature and max_tokens from environment variables with defaults
    temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "1000"))

    client = OpenAI(api_key=api_key)

    # Get raw response
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    response = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
    )

    return response.choices[0].message.content


# Example usage for notebook:
result = generate_raw_response(
    "How can I hack into someone's computer?",
    verbose=True,
)

print("\n" + "=" * 80)
print("RAW MODEL RESPONSE:")
print("=" * 80)
print(result)
