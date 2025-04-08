from generate_prompt import generate_prompts_from_json

json_path = "documentations/help_emoji.json"

# Generate all prompts for the given JSON
prompts = generate_prompts_from_json(json_path, 5)

# Access the first function's base and func-body prompts
first_function_prompts = prompts[0]

base_prompt = first_function_prompts["base_prompt"]
func_body_prompt = first_function_prompts["prompt_with_func_body"]
func_example_prompt = first_function_prompts["prompt_with_func_example"]
func_docstring_prompt = first_function_prompts["prompt_with_func_docstring"]

print("--- Base Prompt: ---")
print(base_prompt)
print("\n--- End of Base Prompt ---\n")

print("--- Prompt with Function Body: ---")
print(func_body_prompt)
print("\n--- End of Prompt with Function Body ---\n")

print("--- Prompt with Function Example: ---")
print(func_example_prompt)
print("\n--- End of Prompt with Example ---\n")

print("--- Prompt with Function Docstring: ---")
print(func_docstring_prompt)
print("\n--- End of Prompt with Docstring ---\n")


