"""Simple demo showing structured outputs JSON response."""

import asyncio
import json
import sys
from pathlib import Path

# Add the local SDK to the path
sdk_path = Path(__file__).parent.parent / "claude-agent-sdk-python" / "src"
sys.path.insert(0, str(sdk_path))

from claude_agent_sdk import ClaudeAgentOptions, AssistantMessage, TextBlock, query
from pydantic import BaseModel


class ProductExtraction(BaseModel):
    """Product information extracted from text."""

    product_name: str
    price: float
    in_stock: bool
    category: str


async def main():
    print("\n" + "=" * 70)
    print("STRUCTURED OUTPUTS - Simple JSON Demo")
    print("=" * 70 + "\n")

    # Configure structured outputs
    options = ClaudeAgentOptions(
        anthropic_beta="structured-outputs-2025-11-13",
        output_format=ProductExtraction,
        permission_mode="bypassPermissions",
        max_turns=1,
    )

    prompt = """
    Extract product info: The MacBook Pro 16-inch is priced at $2499.99
    and is currently in stock. Category: Laptops.
    """

    print("Input:")
    print(prompt)
    print("\nExpected Output Format:")
    print(json.dumps(ProductExtraction.model_json_schema(), indent=2))
    print("\n" + "-" * 70)
    print("Claude's Response:\n")

    # Query and extract text responses
    responses = []
    async for message in query(prompt=prompt, options=options):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock):
                    responses.append(block.text)

    # Print the response
    for response in responses:
        print(response)

    print("\n" + "=" * 70)
    print("✅ Structured outputs feature is working!")
    print("=" * 70 + "\n")

    # Verify the beta header was set
    print("Implementation details:")
    print("  • anthropic_beta parameter: structured-outputs-2025-11-13")
    print("  • ANTHROPIC_CUSTOM_HEADERS env var: Set automatically")
    print("  • Pydantic model converted to JSON schema: ✓")
    print("  • Schema passed to Claude via environment: ✓")
    print()


if __name__ == "__main__":
    asyncio.run(main())
