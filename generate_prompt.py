import json
import os
from typing import Dict, List, Optional
import tiktoken

MAX_TOKENS = 6000  # Aim to stay under this for GPT-4 (safe buffer from 8K)

def estimate_tokens(text: str, model: str = "gpt-4") -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def clean_docstring(docstring: str) -> str:
    if not docstring:
        return ""
    return "\n".join(line.strip() for line in docstring.strip().splitlines())

def build_prompt(item: Dict, include_doc=True, include_examples=True, include_source=True) -> str:
    """
    Builds a smart prompt that includes as much information as possible within GPT token limits.
    """
    type_ = item.get("type", "function")
    qualified_name = item.get("qualified_name", "unknown")
    signature = item.get("signature", "")
    docstring = clean_docstring(item.get("docstring", ""))
    examples = item.get("examples", [])
    source_code = item.get("source_code", "").strip()

    base_prompt = (
        "You are a skilled Python developer. You specialize in writing high-quality unit tests "
        "for open-source Python libraries using `pytest`.\n\n"
        "I will provide you with metadata about a public API. Your task is to generate a **unit test** using `pytest` that:\n"
        "- Uses realistic and meaningful inputs,\n"
        "- Verifies expected behavior through assertions,\n"
        "- Handles edge cases if possible,\n"
        "- Is self-contained and can be executed without modification.\n\n"
    )

    metadata_sections = []

    metadata_sections.append(f"### API Type:\n{type_}\n\n")
    metadata_sections.append(f"### Qualified Name:\n{qualified_name}\n\n")
    metadata_sections.append(f"### Signature:\n{signature}\n\n")

    if include_doc and docstring:
        metadata_sections.append(f"### Docstring:\n\"\"\"\n{docstring}\n\"\"\"\n\n")

    if include_examples and examples:
        limited_examples = examples[:3]
        example_str = "\n".join(limited_examples)
        metadata_sections.append(f"### Example Usage:\n{example_str}\n\n")

    if include_source and source_code:
        metadata_sections.append(f"### Source Code:\n```python\n{source_code}\n```\n")

    closing = "\nNow write a complete unit test using pytest:\n```python\n"

    full_prompt = base_prompt + "".join(metadata_sections) + closing

    # Estimate token count and trim if needed
    tokens = estimate_tokens(full_prompt)

    if tokens > MAX_TOKENS:
        print(f"⚠️ Trimming prompt for {qualified_name} (initial tokens: {tokens})")

        # Trim examples
        metadata_sections = [s for s in metadata_sections if not s.startswith("### Example Usage")]
        tokens = estimate_tokens(base_prompt + "".join(metadata_sections) + closing)

        # Truncate docstring to first 20 lines
        if tokens > MAX_TOKENS and include_doc and docstring:
            doc_lines = docstring.splitlines()
            truncated = "\n".join(doc_lines[:20]) + "\n... (truncated)"
            metadata_sections = [
                s if not s.startswith("### Docstring") else f"### Docstring:\n\"\"\"\n{truncated}\n\"\"\"\n\n"
                for s in metadata_sections
            ]
            tokens = estimate_tokens(base_prompt + "".join(metadata_sections) + closing)

        # Remove source code if still too long
        if tokens > MAX_TOKENS and include_source and source_code:
            metadata_sections = [s for s in metadata_sections if not s.startswith("### Source Code")]
            metadata_sections.append(
                "# Note: Source code omitted due to size. Use docstring and signature for test.\n\n"
            )

    return base_prompt + "".join(metadata_sections) + closing


def generate_prompts_from_json(json_path: str, out_dir: Optional[str] = None) -> List[str]:
    """
    Reads API metadata from a JSON file and generates prompts.
    """
    with open(json_path, "r") as f:
        metadata = json.load(f)

    prompts = []
    for package_name, items in metadata.items():
        for item in items:
            prompt = build_prompt(item)
            prompts.append(prompt)

            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
                filename = item["qualified_name"].replace(".", "_")
                with open(os.path.join(out_dir, f"prompt_{filename}.txt"), "w") as f_out:
                    f_out.write(prompt)

    return prompts

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate LLM prompts from API metadata JSON.")
    parser.add_argument("--json", required=True, help="Path to JSON file with API metadata.")
    parser.add_argument("--out", help="Optional: Output directory to save prompt text files.")
    args = parser.parse_args()

    generate_prompts_from_json(args.json, args.out)

#How to run: generate_prompt.py --json documentations/help_emoji.json --out prompts/