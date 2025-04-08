from generate_prompt import generate_prompts_from_json

json_path = "documentations/help_emoji.json"

# Generate all prompts for the given JSON
prompts = generate_prompts_from_json(json_path, 5)

# Access the first function's base and func-body prompts
first_function_prompts = prompts[0]

base_prompt = first_function_prompts["base_prompt"]
func_body_prompt = first_function_prompts["prompt_with_func_body"]

print("--- Base Prompt: ---")
print(base_prompt)
print("\n--- End of Base Prompt ---\n")

print("--- Prompt with Function Body: ---")
print(func_body_prompt)
print("\n--- End of Prompt with Function Body ---\n")


