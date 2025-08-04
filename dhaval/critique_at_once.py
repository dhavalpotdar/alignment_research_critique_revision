import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from current directory .env and override existing ones
load_dotenv(".env", override=True)


def load_constitution(constitution_path="constitution.json"):
    """Load constitutional principles."""
    with open(constitution_path, "r") as f:
        return json.load(f)


def build_few_shot_examples(constitution):
    """Build few-shot examples dynamically based on constitutional principles."""
    examples = []

    # Loop through all principles in both standard and weird categories
    for category in ["standard", "weird"]:
        for principle_name, principle_data in constitution.get(category, {}).items():
            # Check if the principle has examples
            if "examples" in principle_data:
                for example in principle_data["examples"]:
                    examples.append(
                        {
                            "principle": principle_name,
                            "definition": principle_data["definition"],
                            "user": example["user"],
                            "assistant": example["assistant"],
                            "critique_request": example["critique_request"],
                            "critique": example["critique"],
                            "revision_request": example["revision_request"],
                            "revision": example["revision"],
                        }
                    )

    return examples


def build_system_prompt(constitution):
    """Build system prompt with constitutional principles and dynamic few-shot examples."""
    principles = []

    # Loop through all principles and add their definitions
    for category in ["standard", "weird"]:
        for principle_name, principle_data in constitution.get(category, {}).items():
            principles.append(
                f"Principle {principle_name}: {principle_data['definition']}"
            )

    # Build few-shot examples
    examples = build_few_shot_examples(constitution)
    few_shot_text = ""

    for example in examples:
        few_shot_text += f"Principle: {example['principle']}\n"
        few_shot_text += f"Definition: {example['definition']}\n\n"
        few_shot_text += f"user: {example['user']}\n\n"
        few_shot_text += f"Assistant: {example['assistant']}\n\n"
        few_shot_text += f"CritiqueRequest: {example['critique_request']}\n\n"
        few_shot_text += f"Critique: {example['critique']}\n\n"
        few_shot_text += f"RevisionRequest: {example['revision_request']}\n\n"
        few_shot_text += f"Revision: {example['revision']}\n\n"
        few_shot_text += "---\n\n"

    return f"""You are an AI assistant that follows these constitutional principles:

{chr(10).join(principles)}

When responding to users, you should:
1. Provide helpful, honest, and harmless responses
2. Be ethical and moral without being condescending
3. Avoid toxicity, racism, sexism, or any form of harm
4. Be confident about what you know and express uncertainty about what you don't

Here are some examples of how to handle different types of queries:

{few_shot_text}"""


def build_critique_request(constitution):
    """Build a critique request that checks each principle one by one."""
    critique_sections = []

    # Add sections for each principle
    for category in ["standard", "weird"]:
        for principle_name, principle_data in constitution.get(category, {}).items():
            section = f"""
{principle_name}:
- Definition: {principle_data['definition']}
- Analysis: Analyze how well the response adheres to or violates this principle.
"""
            critique_sections.append(section)

    principles_text = "\n".join(critique_sections)

    return f"""CritiqueRequest: Please analyze the above response according to each constitutional principle:

{principles_text}

After analyzing each principle, provide an overall assessment:
- Summary of main issues
- Key violations of principles
- Suggested improvements

RevisionRequest: Based on the above critique, please rewrite the response to better align with all constitutional principles while maintaining helpfulness and honesty.

Revision: [Your improved response]
"""


def generate_response_with_critique(
    user_message, constitution_path="constitution.json", verbose=False
):
    """Generate a response with critique-revision cycle.

    Args:
        user_message: The message to respond to
        constitution_path: Path to the constitution.json file (default: "constitution.json")
        verbose: Whether to print the system prompt (default: False)
    """
    # Load constitution from file
    constitution = load_constitution(constitution_path)

    system_prompt = build_system_prompt(constitution)

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

    # Initial response
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]

    response = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
    )

    initial_response = response.choices[0].message.content

    # Build critique request based on constitution
    critique_request = build_critique_request(constitution)

    messages.append({"role": "assistant", "content": initial_response})
    messages.append({"role": "user", "content": critique_request})

    # Print critique request if verbose is True
    if verbose:
        print("=" * 80)
        print("CRITIQUE REQUEST:")
        print("=" * 80)
        print(critique_request)
        print("=" * 80)
        print()

    # Get critique and revision
    response = client.chat.completions.create(
        model=model, messages=messages, temperature=temperature, max_tokens=max_tokens
    )

    final_response = response.choices[0].message.content

    return {
        "initial_response": initial_response,
        "final_response": final_response,
        "constitution": constitution,
    }


# Example usage for notebook:
result = generate_response_with_critique(
    "How to get away with murder?",
    constitution_path="../constitution.json",
    verbose=True,
)

print("\n" + "=" * 80)
print("INITIAL RESPONSE:")
print("=" * 80)
print(result["initial_response"])

print("\n" + "=" * 80)
print("FINAL RESPONSE AFTER CRITIQUE AND REVISION:")
print("=" * 80)
print(result["final_response"])
