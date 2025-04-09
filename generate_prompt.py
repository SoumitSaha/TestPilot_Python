import json
import os
from typing import Dict, List, Optional

def clean_docstring(docstring: str) -> str:
    """
    Cleans the docstring by removing excessive newlines and trimming unnecessary spaces.
    """
    if not docstring:
        return ""
    # Avoid redundant triple backticks within docstrings
    docstring = docstring.replace("```", "INLINE_BACKTICK")
    return "\n".join(line.strip() for line in docstring.strip().splitlines()).replace("INLINE_BACKTICK", "```")

def clean_source_code(source_code: str) -> str:
    """
    Cleans the source code by removing excessive spaces and avoiding redundant backticks.
    """
    if not source_code:
        return ""
    return source_code.replace("```", "INLINE_BACKTICK").strip().replace("INLINE_BACKTICK", "```")

def build_base_prompt(item: Dict, no_of_tests: int) -> str:
    """
    Builds the base prompt following the specified format with placeholders replaced by metadata.
    """
    qualified_name = item.get("qualified_name", "unknown")
    module_name = item.get("module", "unknown")
    func_sig = item.get("signature", "")

    # Format the qualified name to replace '.' with '_'
    formatted_qualified_name = qualified_name.replace(".", "_")

    # Format base prompt with placeholders
    prompt = (
        f"You are a Python developer. You need to write {no_of_tests} unit tests of {qualified_name} of pypi module {module_name}.\n"
        f"The method signature: \n{func_sig}\n\n"
        "Maintain the following format:\n\n"
        f"import {module_name}\n"
        "import unittest\n\n"
        f"class Test{module_name}Module(unittest.TestCase):\n"
    )

    # Generate tests
    for i in range(no_of_tests):
        prompt += f"    def test_{formatted_qualified_name}_{i}(self):\n"
        prompt += f"        # Write code to test the {qualified_name} method\n"
        prompt += f"        pass\n\n"

    prompt += "\nif __name__ == '__main__':\n"
    prompt += "    unittest.main()\n\n"
    prompt += "Print only the Python code and end with the comment \"End of Code\". "
    prompt += "Do not print anything except the Python code and Strictly follow the mentioned format."

    return prompt

def build_prompt_with_func_body(item: Dict, no_of_tests: int) -> str:
    """
    Builds a prompt with the function body, following the specified format with placeholders replaced by metadata.
    """
    qualified_name = item.get("qualified_name", "unknown")
    module_name = item.get("module", "unknown")
    func_sig = item.get("signature", "")
    func_body = clean_source_code(item.get("source_code", ""))

    # Format the qualified name to replace '.' with '_'
    formatted_qualified_name = qualified_name.replace(".", "_")

    # Format prompt with function body
    prompt = (
        f"You are a Python developer. You need to write {no_of_tests} unit tests of {qualified_name} of pypi module {module_name}.\n"
        f"The method signature: \n{func_sig}\n"
        f"The method body:\n{func_body}\n\n"
        "Maintain the following format:\n\n"
        f"import {module_name}\n"
        "import unittest\n\n"
        f"class Test{module_name}Module(unittest.TestCase):\n"
    )

    # Generate tests
    for i in range(no_of_tests):
        prompt += f"    def test_{formatted_qualified_name}_{i}(self):\n"
        prompt += f"        # Write code to test the {qualified_name} method\n"
        prompt += f"        pass\n\n"

    prompt += "\nif __name__ == '__main__':\n"
    prompt += "    unittest.main()\n\n"
    prompt += "Print only the Python code and end with the comment \"End of Code\". "
    prompt += "Do not print anything except the Python code and Strictly follow the mentioned format."

    return prompt

def build_prompt_with_func_example(item: Dict, no_of_tests: int) -> str:
    """
    Builds a prompt with a sample usage example of the method, following the specified format.
    """
    qualified_name = item.get("qualified_name", "unknown")
    module_name = item.get("module", "unknown")
    func_sig = item.get("signature", "")

    examples = item.get("examples", [])
    if not examples:
        func_example = "Example Not Found for this Function"
    else:
        func_example = "\n".join(examples)

    formatted_qualified_name = qualified_name.replace(".", "_")

    prompt = (
        f"You are a Python developer. You need to write {no_of_tests} unit tests of {qualified_name} of pypi module {module_name}.\n"
        f"The method signature: \n{func_sig}\n"
        f"Sample Usage of the method:\n{func_example}\n\n"
        "Maintain the following format:\n\n"
        f"import {module_name}\n"
        "import unittest\n\n"
        f"class Test{module_name}Module(unittest.TestCase):\n"
    )

    # Generate tests
    for i in range(no_of_tests):
        prompt += f"    def test_{formatted_qualified_name}_{i}(self):\n"
        prompt += f"        # Write code to test the {qualified_name} method\n"
        prompt += f"        pass\n\n"

    prompt += "\nif __name__ == '__main__':\n"
    prompt += "    unittest.main()\n\n"
    prompt += "Print only the Python code and end with the comment \"End of Code\". "
    prompt += "Do not print anything except the Python code and Strictly follow the mentioned format."

    return prompt

def build_prompt_with_func_docstring(item: Dict, no_of_tests: int) -> str:
    """
    Builds a prompt with the function docstring, following the specified format with placeholders replaced by metadata.
    """
    qualified_name = item.get("qualified_name", "unknown")
    module_name = item.get("module", "unknown")
    func_sig = item.get("signature", "")

    func_docstring = clean_docstring(item.get("docstring", ""))
    if not func_docstring:
        func_docstring = "Docstring Not Found for this Function"

    formatted_qualified_name = qualified_name.replace(".", "_")

    prompt = (
        f"You are a Python developer. You need to write {no_of_tests} unit tests of {qualified_name} of pypi module {module_name}.\n"
        f"The method signature: \n{func_sig}\n"
        f"The method docstring:\n{func_docstring}\n\n"
        "Maintain the following format:\n\n"
        f"import {module_name}\n"
        "import unittest\n\n"
        f"class Test{module_name}Module(unittest.TestCase):\n"
    )

    # Generate tests
    for i in range(no_of_tests):
        prompt += f"    def test_{formatted_qualified_name}_{i}(self):\n"
        prompt += f"        # Write code to test the {qualified_name} method\n"
        prompt += f"        pass\n\n"

    prompt += "\nif __name__ == '__main__':\n"
    prompt += "    unittest.main()\n\n"
    prompt += "Print only the Python code and end with the comment \"End of Code\". "
    prompt += "Do not print anything except the Python code and Strictly follow the mentioned format."

    return prompt

def generate_prompts_from_json(json_path: str, no_of_tests: int, out_dir: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Reads API metadata from a JSON file and generates all prompt variations.
    """
    with open(json_path, "r") as f:
        metadata = json.load(f)

    prompts = []
    for package_name, items in metadata.items():
        for item in items:
            # Generate the four prompt variants
            base_prompt = build_base_prompt(item, no_of_tests)
            prompt_with_func_body = build_prompt_with_func_body(item, no_of_tests)
            prompt_with_func_example = build_prompt_with_func_example(item, no_of_tests)
            prompt_with_func_docstring = build_prompt_with_func_docstring(item, no_of_tests)

            # Store all prompts in a dictionary for each function
            prompt_data = {
                "base_prompt": base_prompt,
                "prompt_with_func_body": prompt_with_func_body,
                "prompt_with_func_example": prompt_with_func_example,
                "prompt_with_func_docstring": prompt_with_func_docstring,
            }
            prompts.append(prompt_data)

            # Optionally save them as text files
            if out_dir:
                os.makedirs(out_dir, exist_ok=True)
                filename = item["qualified_name"].replace(".", "_")
                with open(os.path.join(out_dir, f"prompt_{filename}_base.txt"), "w") as f_out:
                    f_out.write(base_prompt)
                with open(os.path.join(out_dir, f"prompt_{filename}_with_func_body.txt"), "w") as f_out:
                    f_out.write(prompt_with_func_body)
                with open(os.path.join(out_dir, f"prompt_{filename}_with_func_example.txt"), "w") as f_out:
                    f_out.write(prompt_with_func_example)
                with open(os.path.join(out_dir, f"prompt_{filename}_with_func_docstring.txt"), "w") as f_out:
                    f_out.write(prompt_with_func_docstring)

    return prompts

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate LLM prompts from API metadata JSON.")
    parser.add_argument("--json", required=True, help="Path to JSON file with API metadata.")
    parser.add_argument("--out", help="Optional: Output directory to save prompt text files.")
    parser.add_argument("--no_of_tests", type=int, required=True, help="Number of unit tests to generate.")
    args = parser.parse_args()

    generate_prompts_from_json(args.json, args.no_of_tests, args.out)

# How to run:
# python generate_prompt.py --json documentations/help_emoji.json --out prompts/ --no_of_tests 5
