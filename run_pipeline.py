import Compiler
import subprocess
import os
import json
import utility
import get_response_from_GPT4

def validate(response_file):
    cmd = f"python \"{response_file}\""
    try:
        subprocess.run(cmd, check=True, capture_output=True, shell=True, timeout=100)
        return None
    except subprocess.CalledProcessError as e:
        return e.stderr.decode()

def throw(prompt, response_file):
    if os.path.exists(response_file):
        pass
    else:
        response = get_response_from_GPT4.generate_using_OPENAI(prompt, "gpt-4")

        with open(response_file, "w") as f:
            print(response, file=f)
            f.close()
        utility.wait_for_file(response_file)

def correction(test_code_fp, test_error, current_iteration, max_iteration, module, formatted_qualified_name, prompt_type):
    if current_iteration > max_iteration:
        return test_code_fp
    
    if test_error is None:
        return test_code_fp
    
    refined_prompt_dir = f"{os.getcwd()}/refined_prompts/{module}"
    os.makedirs(refined_prompt_dir, exist_ok=True)
    refined_prompt_fp = f"{refined_prompt_dir}/refined_prompt_{formatted_qualified_name}_{prompt_type}_it{current_iteration}.txt"

    test_code = utility.load_file_content(test_code_fp)
    prompt = f"{test_code}\nWhen we run the code following error occurs:\n{test_error}\nFix the error.\nPrint only the Python code and end with the comment \"#End of Code\". Do not change any method signature, do not print anything except the Python code, Strictly follow the mentioned format."

    with open(refined_prompt_fp, "w") as f:
        print(prompt, file=f)
        f.close()
    utility.wait_for_file(refined_prompt_fp)

    response_dir = f"{os.getcwd()}/refined_LLM_Responses/{module}"
    os.makedirs(response_dir, exist_ok=True)
    refined_response_fp = f"{response_dir}/refined_response_{formatted_qualified_name}_{prompt_type}_it{current_iteration}.py"

    throw(prompt, refined_response_fp)
    test_error = validate(refined_response_fp)
    return correction(refined_response_fp, test_error, current_iteration+1, max_iteration, module, formatted_qualified_name, prompt_type)


modules = ["emoji", "pyfiglet", "pytz", "shortuuid", "yarl"]

# Generate prompts (base, with function body, docstring, examples) for all modules' public functions
for module in modules:
    try:
        subprocess.run("python generate_prompt.py --json documentations/help_" + module + ".json --out prompts/" + module + " --no_of_tests 5", check=True, capture_output=True, shell=True, timeout=100)
    except Exception as e:
        print(e)
        quit()


# Run whole pipeline
max_refine_iteration = 3

for module in modules:
    documentation_json = f"{os.getcwd()}/documentations/help_{module}.json"

    with open(documentation_json, "r") as f:
        metadata = json.load(f)

    for package_name, items in metadata.items():
        for item in items:
            module_name = package_name
            qualified_name = item.get("qualified_name", "unknown")
            formatted_qualified_name = qualified_name.replace(".", "_")
            prompt_base_fp = f"{os.getcwd()}/prompts/{module}/prompt_{formatted_qualified_name}_base.txt"
            prompt_with_func_body_fp = f"{os.getcwd()}/prompts/{module}/prompt_{formatted_qualified_name}_with_func_body.txt"
            prompt_with_func_example_fp = f"{os.getcwd()}/prompts/{module}/prompt_{formatted_qualified_name}_with_func_example.txt"
            prompt_with_func_docstring_fp = f"{os.getcwd()}/prompts/{module}/prompt_{formatted_qualified_name}_with_func_docstring.txt"

            response_dir = f"{os.getcwd()}/LLM_Responses/{module}"
            os.makedirs(response_dir, exist_ok=True)
            response_base_fp = f"{response_dir}/response_{formatted_qualified_name}_base.py"
            response_with_func_body_fp = f"{response_dir}/response_{formatted_qualified_name}_with_func_body.py"
            response_with_func_example_fp = f"{response_dir}/response_{formatted_qualified_name}_with_func_example.py"
            response_with_func_docstring_fp = f"{response_dir}/response_{formatted_qualified_name}_with_func_docstring.py"

            base_prompt = utility.load_file_content(prompt_base_fp)
            prompt_with_func_body = utility.load_file_content(prompt_with_func_body_fp)
            prompt_with_func_example = utility.load_file_content(prompt_with_func_example_fp)
            prompt_with_func_docstring =utility.load_file_content(prompt_with_func_docstring_fp)

            throw(base_prompt, response_base_fp)
            test_error = validate(response_base_fp)
            correction(response_base_fp, test_error, 1, max_refine_iteration, module, formatted_qualified_name, "base")

            throw(prompt_with_func_body, response_with_func_body_fp)
            test_error = validate(response_with_func_body_fp)
            correction(response_with_func_body_fp, test_error, 1, max_refine_iteration, module, formatted_qualified_name, "with_func_body")

            throw(prompt_with_func_docstring, response_with_func_docstring_fp)
            test_error = validate(response_with_func_docstring_fp)
            correction(response_with_func_docstring_fp, test_error, 1, max_refine_iteration, module, formatted_qualified_name, "with_func_docstring")

            throw(prompt_with_func_example, response_with_func_example_fp)
            test_error = validate(response_with_func_example_fp)
            correction(response_with_func_example_fp, test_error, 1, max_refine_iteration, module, formatted_qualified_name, "with_func_example")

