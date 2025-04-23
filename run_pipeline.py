from tqdm import tqdm
import subprocess
import os
import json
import utility
import get_response_from_GPT4
import ast

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
        response = get_response_from_GPT4.generate_using_OPENAI(prompt, "gpt-4o-mini")
        with open(response_file, "w") as f:
            print(response, file=f)
            f.close()
        utility.wait_for_file(response_file)

def correction(test_code_fp, test_error, current_iteration, max_iteration, module, qualified_name, prompt_type):
    if current_iteration > max_iteration:
        return test_code_fp
    
    if test_error is None:
        return test_code_fp
    
    formatted_qualified_name = qualified_name.replace(".", "_")

    refined_prompt_dir = f"{os.getcwd()}/refined_prompts/{module}"
    os.makedirs(refined_prompt_dir, exist_ok=True)
    refined_prompt_fp = f"{refined_prompt_dir}/refined_prompt_{formatted_qualified_name}_{prompt_type}_it{current_iteration}.txt"

    test_code = utility.load_file_content(test_code_fp)
    prompt = f"{test_code}\nThe unittest code to test {qualified_name} has following error(s):\n{test_error}\nFix the error. (Note that the {qualified_name} function exits in {module}. So, do not add any new function to the code on your own. Try to fix assertion errors. Our main target is to write correct unittest code for {qualified_name})\nPrint only the Python code and end with the comment \"#End of Code\". Do not change any method signature, do not print anything except the Python code, Strictly follow the mentioned format."

    with open(refined_prompt_fp, "w") as f:
        print(prompt, file=f)
        f.close()
    utility.wait_for_file(refined_prompt_fp)

    response_dir = f"{os.getcwd()}/refined_LLM_Responses/{module}"
    os.makedirs(response_dir, exist_ok=True)
    refined_response_fp = f"{response_dir}/refined_response_{formatted_qualified_name}_{prompt_type}_it{current_iteration}.py"

    throw(prompt, refined_response_fp)
    test_error = validate(refined_response_fp)
    return correction(refined_response_fp, test_error, current_iteration+1, max_iteration, module, qualified_name, prompt_type)


modules = ["emoji", "pyfiglet", "pytz", "shortuuid", "yarl"]

# Generate prompts (base, with function body, docstring, examples) for all modules' public functions
for module in modules:
    if not os.path.exists(f"{os.getcwd()}/prompts/{module}"):
        try:
            subprocess.run("python generate_prompt.py --json documentations/help_" + module + ".json --out prompts/" + module + " --no_of_tests 5", check=True, capture_output=True, shell=True, timeout=100)
        except Exception as e:
            print(e)
            quit()
    else:
        print(f"{module}: Documentation already exists")

# Run whole pipeline
max_refine_iteration = 3

for module in tqdm(modules, desc="Modules"):
    documentation_json = f"{os.getcwd()}/documentations/help_{module}.json"

    with open(documentation_json, "r") as f:
        metadata = json.load(f)

    for package_name, items in metadata.items():
        for item in tqdm(items, desc=f"Items in {package_name}", leave=False):
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
            correction(response_base_fp, test_error, 1, max_refine_iteration, module, qualified_name, "base")

            throw(prompt_with_func_body, response_with_func_body_fp)
            test_error = validate(response_with_func_body_fp)
            correction(response_with_func_body_fp, test_error, 1, max_refine_iteration, module, qualified_name, "with_func_body")

            throw(prompt_with_func_docstring, response_with_func_docstring_fp)
            test_error = validate(response_with_func_docstring_fp)
            correction(response_with_func_docstring_fp, test_error, 1, max_refine_iteration, module, qualified_name, "with_func_docstring")

            throw(prompt_with_func_example, response_with_func_example_fp)
            test_error = validate(response_with_func_example_fp)
            correction(response_with_func_example_fp, test_error, 1, max_refine_iteration, module, qualified_name, "with_func_example")

# Merge all the passing unittests for each module in a single file
doc_dir = f"{os.getcwd()}/documentations/"
response_dir = f"{os.getcwd()}/LLM_Responses/"
refined_response_dir = f"{os.getcwd()}/refined_LLM_Responses/"

for module in modules:
    required_files = utility.find_best_test_files(doc_dir, response_dir, refined_response_dir, module, max_refine_iteration)

    imports = set()
    class_definitions = []
    class_prefix = f"Test{module}Module"

    for idx, file in enumerate(required_files):
        passing_methods_in_file = utility.list_passing_methods_of_file(file)

        if not passing_methods_in_file:
            continue

        with open(file, "r") as f:
            tree = ast.parse(f.read(), filename=file)

        for node in tree.body:
            # Collect top-level imports
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                imports.add(ast.unparse(node))

            # Locate the test class
            elif isinstance(node, ast.ClassDef) and node.name == class_prefix:
                new_class_name = f"{class_prefix}FromFile{idx}"
                new_class = ast.ClassDef(
                    name=new_class_name,
                    bases=node.bases,
                    keywords=node.keywords if hasattr(node, 'keywords') else [],
                    decorator_list=node.decorator_list,
                    body=[]
                )

                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if item.name in passing_methods_in_file or item.name.startswith("setUp") or item.name.startswith("tearDown"):
                            new_class.body.append(item)

                if new_class.body:
                    class_definitions.append(new_class)

    # Save to final merged test file
    save_dir = f"{os.getcwd()}/Merged_Response/{module}"
    os.makedirs(save_dir, exist_ok=True)
    output_path = f"{save_dir}/test_{module}_merged.py"

    with open(output_path, "w") as out:
        out.write("import unittest\n")
        out.write("\n".join(imports))
        out.write("\n\n")

        for class_node in class_definitions:
            class_code = ast.unparse(class_node)
            out.write(class_code + "\n\n")

        out.write("if __name__ == '__main__':\n")
        out.write("    unittest.main()\n")

# Generate coverage for each module
merged_file_dir = f"{os.getcwd()}/Merged_Response"
for module in modules:
    merged_file = f"{merged_file_dir}/{module}/test_{module}_merged.py"
    cmd = f"pytest --cov={module} --cov-branch --cov-report=xml:coverage_{module}.xml -s -q --tb=short {merged_file}"
    try:
        subprocess.run(cmd, check=True, capture_output=True, shell=True, timeout=100)
    except subprocess.CalledProcessError as e:
        print(e.stderr.decode())


# # Give branch and statement coverage for the modules
# for module in modules:
#     cmd = f"python find_cumulative_coverage.py --xml coverage_{module}.py"
#     try:
#         subprocess.run(cmd, check=True, capture_output=True, shell=True, timeout=100)
#     except subprocess.CalledProcessError as e:
#         print(e.stderr.decode())