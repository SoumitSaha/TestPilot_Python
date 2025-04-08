from generate_prompt import generate_prompts_from_json

json_path = "documentations/help_emoji.json"

# Generate all prompts for the given JSON
prompts = generate_prompts_from_json(json_path, 5)


# Each function has two prompts, base and with function body

def print_prompts_for_function(function_index):
    base_prompt = prompts[function_index * 2]  # Base prompt is at even index (0, 2, 4, ...)
    func_body_prompt = prompts[function_index * 2 + 1]  # Prompt with function body is at odd index (1, 3, 5, ...)

    print("Base Prompt:")
    print(base_prompt)
    print("\n--- End of Base Prompt ---\n")

    print("Prompt with Function Body:")
    print(func_body_prompt)
    print("\n--- End of Prompt with Function Body ---\n")


# Print both prompts for the first function (function_index 0)
print_prompts_for_function(1)
