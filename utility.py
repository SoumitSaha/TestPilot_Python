import time
import os
import subprocess
from pathlib import Path
import shutil
import Compiler
import Constants
import json
import re

def extract_code_snippets(text):
    """
    Extracts all code snippets enclosed in triple backticks from the text.
    If no such blocks exist, treats the whole text as a single code snippet.
    """
    code_blocks = re.findall(r'```(?:[\w+]*\n)?(.*?)```', text, re.DOTALL)
    code_blocks = [block.strip() for block in code_blocks]

    if not code_blocks:
        # If no backticks, treat the entire text as a code snippet if it looks like code
        if looks_like_code(text):
            code_blocks.append(text.strip())

    return code_blocks

def looks_like_code(text):
    """
    A simple heuristic to decide if a text looks like code:
    - Contains multiple lines
    - Has typical code patterns (like 'def', 'class', '=', 'import', 'return', braces, etc.)
    """
    code_keywords = ['def ', 'class ', 'import ', 'return', 'if ', 'else', '=', 'for ', 'while ', '(', ')', '{', '}', ':']
    lines = text.strip().splitlines()
    if len(lines) < 2:
        return False
    score = sum(any(kw in line for kw in code_keywords) for line in lines)
    return score / len(lines) > 0.3  # at least 30% of lines should look like code

def get_longest_code_snippet(text):
    """
    Returns the longest code snippet from the text.
    """
    code_snippets = extract_code_snippets(text)
    if not code_snippets:
        return None
    return max(code_snippets, key=len)

def load_dict_from_file(file_location):
    if os.path.isfile(file_location):
        with open(file_location, "r") as f:
            try:
                data = json.load(f)
                f.close()
                return data
            except:
                return None
    return None

def get_top_n_lines(code_file, file_path, n):
    try:
        # Read the JSON file
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Convert the dictionary into a list of tuples and sort by score in descending order
        sorted_lines = sorted(data.items(), key=lambda item: item[1], reverse=True)
        
        # Collect lines based on scores
        top_n_lines = []
        score_groups = {}
        
        for line, score in sorted_lines:
            if score == 0:  # Skip lines with a score of 0
                continue
            if score not in score_groups:
                score_groups[score] = []
            score_groups[score].append(int(line) - 1)  # Convert line number to zero-based
        
        # Add lines from groups until n is reached
        for score, lines in score_groups.items():
            if len(top_n_lines) + len(lines) <= n:
                top_n_lines.extend(lines)
            else:
                top_n_lines.extend(lines[:n - len(top_n_lines)])
                break
        
        # Sort the line numbers in ascending order
        top_n_lines_sorted = sorted(top_n_lines)
        
        # Read the code file
        with open(code_file, "r") as file:
            lines = file.readlines()
        
        # Retrieve the lines from the file corresponding to the top scores
        result = [lines[line_num] for line_num in top_n_lines_sorted]
        
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []


# def get_top_n_lines(code_file, file_path, n):
#     try:
#         # Read the JSON file
#         with open(file_path, 'r') as file:
#             data = json.load(file)
        
#         # Convert the dictionary into a list of tuples and sort by score in descending order
#         sorted_lines = sorted(data.items(), key=lambda item: item[1], reverse=True)
        
#         # Get the top n lines
#         top_n_lines = sorted_lines[:n]
        
#         # Sort the line numbers in ascending order (adjusted for zero-based indexing)
#         top_n_lines_sorted = sorted(int(line) - 1 for line, score in top_n_lines)

#         # Read the code file
#         with open(code_file, "r") as file:
#             lines = file.readlines()
        
#         # Retrieve the lines from the file corresponding to the top scores
#         result = [lines[line_num] for line_num in top_n_lines_sorted]
        
#         return result
#     except Exception as e:
#         print(f"Error: {e}")
#         return []

def load_file_content(file):
    content = None
    with open(file, "r") as f:
        content = f.read()
        f.close()
    return content

def remove_Tuple_class(code_snippet):
    index = code_snippet.find("class Tuple")
    if index != -1:

        prev_part = code_snippet[:index]

        last_curly_end = prev_part.rfind("}")
        prev_part = code_snippet[:last_curly_end + 1]
        last_part = code_snippet[index:]
        no_of_curly = 1
        opening_curly = last_part.find("{")
        last_part = last_part[opening_curly:]

        tuple_end_at = -1

        for i in range(1, len(last_part), 1):
            if last_part[i] == "{":
                no_of_curly += 1
            elif last_part[i] == "}":
                no_of_curly -= 1

            if no_of_curly == 0:
                tuple_end_at = i
                break

        if tuple_end_at != -1:
            last_part = last_part[tuple_end_at + 1:]

        return prev_part + "\n" + last_part, True
    else:
        return code_snippet, False

def wait_for_file(filepath, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        if os.path.exists(filepath):
            return True
        time.sleep(0.1)
    return False

def compile_junit(jar_location, source_files):
    junit_jar = f"{jar_location}/junit-4.13.2.jar"
    hamcrest_jar = f"{jar_location}/hamcrest-core-1.3.jar"
    temp_dir = f"{os.getcwd()}/temp_dir"
    os.makedirs(temp_dir, exist_ok=True)

    for file in source_files:
        shutil.copy(file, temp_dir)

    compile_cmd = f"javac -cp {junit_jar}:{hamcrest_jar}"

    for file in source_files:
        compile_cmd = compile_cmd + f" {str(Path(file).name)}"

    current_dir = f"{os.getcwd()}"
    os.chdir(temp_dir)
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, shell=True, timeout=100)
    except subprocess.CalledProcessError as e:
        shutil.rmtree(temp_dir)
        os.chdir(current_dir)
        return Constants.COMPILATION_ERROR, e.stderr.decode()

    os.chdir(current_dir)
    shutil.rmtree(temp_dir)
    return Constants.COMPILATION_SUCCESS, None

def run_junit(jar_location, source_files, test_file):
    junit_jar = f"{jar_location}/junit-4.13.2.jar"
    hamcrest_jar = f"{jar_location}/hamcrest-core-1.3.jar"
    temp_dir = f"{os.getcwd()}/temp_dir"

    os.makedirs(temp_dir, exist_ok=True)

    for file in source_files:
        shutil.copy(file, temp_dir)

    compile_cmd = f"javac -cp {junit_jar}:{hamcrest_jar}"

    for file in source_files:
        compile_cmd = compile_cmd + f" {str(Path(file).name)}"

    current_dir = f"{os.getcwd()}"
    os.chdir(temp_dir)
    try:
        subprocess.run(compile_cmd, check=True, capture_output=True, shell=True, timeout=100)
    except subprocess.CalledProcessError as e:
        print("==============================", e.stderr.decode(), "==============================", e.stdout.decode(), "==============================")
    run_cmd = f"java -cp {junit_jar}:{hamcrest_jar}:{temp_dir} org.junit.runner.JUnitCore {str(Path(test_file).stem)}"
    try:
        result = subprocess.run(run_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, shell=True, timeout=100)
    except subprocess.CalledProcessError as e:
        shutil.rmtree(temp_dir)
        os.chdir(current_dir)
        print("all_passed False run_junit")
        return False, e.stdout.decode()

    os.chdir(current_dir)
    shutil.rmtree(temp_dir)
    print("all_passed True run_junit")
    return True, result.stdout.decode()

def compile_code(code_content, code_file_name, target_lang, temp_dir):
    current_dir = os.getcwd()
    temp_dir_translation = f"{temp_dir}/temp_compilation"
    os.makedirs(temp_dir_translation, exist_ok=True)
    os.chdir(temp_dir_translation)
    with open(f"{temp_dir_translation}/{code_file_name}", "w") as f:
        print(code_content, file=f)
        f.close()
    tracked_files = set(os.listdir(temp_dir_translation))
    compile_success, error_info = Compiler.compile(temp_dir_translation, code_file_name, target_lang)
    generated_binary_files = set(os.listdir(temp_dir_translation)) - tracked_files
    for file in generated_binary_files:
        if not os.path.isdir(f"{temp_dir_translation}/{file}"):
            os.remove(f"{temp_dir_translation}/{file}")
        else:
            shutil.rmtree(f"{temp_dir_translation}/{file}")
    os.chdir(current_dir)
    shutil.rmtree(temp_dir_translation)
    return compile_success, error_info

def test_translated_codes(translated_code_content, code_file_name, target_lang, temp_dir, input_content, output_content):
    current_dir = os.getcwd()
    temp_dir_translation = f"{temp_dir}/temp_compilation"
    os.makedirs(temp_dir_translation, exist_ok=True)
    os.chdir(temp_dir_translation)
    with open(f"{temp_dir_translation}/{code_file_name}", "w") as f:
        print(translated_code_content, file=f)
        f.close()
    tracked_files = set(os.listdir(temp_dir_translation))
    verdict, error_info, _ = Compiler.test(temp_dir_translation, code_file_name, input_content, output_content, target_lang)
    generated_binary_files = set(os.listdir(temp_dir_translation)) - tracked_files
    for file in generated_binary_files:
        if not os.path.isdir(f"{temp_dir_translation}/{file}"):
            os.remove(f"{temp_dir_translation}/{file}")
        else:
            shutil.rmtree(f"{temp_dir_translation}/{file}")
    os.chdir(current_dir)
    shutil.rmtree(temp_dir_translation)
    return verdict, error_info

def generate_error_info_from_verdict(verdict_errorinfo_arr):
    for verdict_errinfo in verdict_errorinfo_arr:
        verdict = verdict_errinfo[0]
        err_info = verdict_errinfo[1]

def should_consider_this_sample_in_this_phase_and_generate_test(prev_report):
    if not "base_translation" in prev_report:
        return True, True
    if "base_translation_compilation_success" in prev_report and "all_test_passed_after_compile_fixation" in prev_report:
        if prev_report["base_translation_compilation_success"] == True:
            if prev_report["all_test_passed_after_compile_fixation"] == True:
                return False, False
            else:
                if prev_report["all_test_passed_after_other_fixation"] == True:
                    return False, False
                else:
                    return True, False
        else:
            if prev_report["compilation_error_fixed"] == False:
                return True, True
            else:
                if "all_test_passed_after_compile_fixation" in prev_report:
                    if prev_report["all_test_passed_after_compile_fixation"] == True:
                        return False, False
                    else:
                        if prev_report["all_test_passed_after_other_fixation"] == True:
                            return False, False
                        else:
                            return True, False
    else:
        return True, True
    

    import re