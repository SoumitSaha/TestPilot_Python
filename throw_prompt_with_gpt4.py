import os
import openai
import tiktoken
from dotenv import load_dotenv
import utility

def load_api_key():
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    return

def load_source_content(source_file):
    content = None
    with open(source_file, "r") as f:
        content = f.read()
    return content

def send_message_to_openai(message, model):
    load_api_key()
    "Use OpenAI's ChatCompletion API to get the chatbot's response"
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(message[1]["content"]))

    response = "exceptional case"
    is_success = False
    max_attempts = 5
    while max_attempts > 0:
        try:
            response = openai.ChatCompletion.create(
                model=model,  # The name of the OpenAI chatbot model to use
                messages=message,  # The conversation history up to this point, as a list of dictionaries
                max_tokens=max(1, 8000 - num_tokens),  # The maximum number of tokens (words or subwords) in the generated response
                temperature=0.7,  # The "creativity" of the generated response (higher temperature = more creative)
            )
            is_success = True
            break
        except Exception as e:
            print(f"Error: {e}")
            max_attempts -= 1
            continue

    if not is_success:
        return response

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message['content']

def generate_using_OPENAI(content, model, target_lang):
    message = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}
    ]
    response = send_message_to_openai(message, model).replace(f"```{target_lang.lower()}", "").replace(f"```cpp", "").replace("```", "")
    return response

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get cumulative coverage from a .xml coverage report")
    parser.add_argument("--prompt_file", required=True, help="Path to prompt file")
    parser.add_argument("--response_dir", required=True, help="Directory to response save")
    parser.add_argument("--response_file", required=True, help="Response save filename")
    args = parser.parse_args()

    prompt_file = f"{os.getcwd()}/{args.prompt_file}"
    response_dir = f"{os.getcwd()}/{args.response_dir}"
    fname = f"{response_dir}/{args.response_file}"
    try:
        with open(prompt_file, "r") as f:
            content = f.read()
    except Exception as e:
        print(f"Error: {e}")
        print("Invalid Prompt File. Program exit.")
        exit()

    response = generate_using_OPENAI(content, "gpt-4", "Python")

    os.makedirs(response_dir, exist_ok=True)
    with open(fname, "w") as f:
        f.write(response)

# How to use this file:
# python throw_prompt_with_gpt4.py --prompt_file prompts/prompt_emoji_core_demojize_base.txt --response_dir LLM_Responses --response_file response_emoji_core_demojize_base_gpt4.py
