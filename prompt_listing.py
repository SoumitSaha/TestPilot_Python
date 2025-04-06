from generate_prompt import generate_prompts_from_json

json_path = "documentations/help_emoji.json"

prompts = generate_prompts_from_json(json_path)

print(prompts[0])

#for i, prompt in enumerate(prompts):
#    print(f"\n--- Prompt {i+1} ---\n")
#    print(prompt)