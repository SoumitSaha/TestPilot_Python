import os
import openai
from openai import OpenAI
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
        f.close()
    return content

def send_message_to_openai(message, model):
    load_api_key()
    "Use OpenAI's ChatCompletion API to get the chatbot's response"
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = len(encoding.encode(message[1]["content"]))

    response = "exceptional case"
    is_success = False
    max_attempts = 5
    client = OpenAI()
    while max_attempts > 0:
        try:
            response = client.chat.completions.create(
                model = model,  # The name of the OpenAI chatbot model to use
                # The conversation history up to this point, as a list of dictionaries
                messages = message,
                # The maximum number of tokens (words or subwords) in the generated response
                max_tokens = max(1, 8000 - num_tokens),
                # The "creativity" of the generated response (higher temperature = more creative)
                temperature=0.7,
            )
            is_success = True
            break
        except:
            max_attempts -= 1
            continue

    if not is_success:
        return response

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content

def generate_using_OPENAI(content, model, target_lang):
    message = [
        {"role": "system", "content": "You are a Python developer and an expert Unit Test Generator."},
        {"role": "user", "content": content}]
    response = send_message_to_openai(message, model).replace(f"```{target_lang.lower()}", "").replace(f"```cpp", "").replace("```", "")
    return response

