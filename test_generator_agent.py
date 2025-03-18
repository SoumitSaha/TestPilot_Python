import os
import openai
from openai import OpenAI
import tiktoken
from dotenv import load_dotenv
import re
from pathlib import Path
from subprocess import Popen, PIPE
import Compiler
import Constants
import utility

ext_to_lang = {
    "py": "Python",
    "java": "Java",
    "c": "C",
    "cpp": "C++",
    "go": "Go"
}

lang_to_ext = {
    "Python": "py",
    "Java": "java",
    "C": "c",
    "C++": "cpp",
    "Go": "go"
}

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

def generate_test_cases_with_OPENAI(content, model):
    message = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": content}]
    response = send_message_to_openai(message, model)
    return response.replace("```", "")

def get_test_details(test):
    regex = r"(\w+):\s+self\.(\w+)\((.+?),\s+(\w+)\((.*)\)\)"
    match = re.match(regex, test)
    error = False
    if match:
        test_name = match.group(1)          # test_0
        assert_method = match.group(2)      # assertEqual
        expected_output = match.group(3)    # 0.0
        test_func = match.group(4)          # truncate_number
        func_input = match.group(5)         # 1000000000.0
    else:
        error = True

    dict = {}

    if error:
        return False, {}
    else:
        dict["test_name"] = test_name
        dict["assert_method"] = f"self.{assert_method}"
        dict["expected_output"] = expected_output
        dict["test_func"] = test_func
        dict["func_input"] = func_input
        return True, dict

def extract_all_tests(unit_test_file):
    file_test_results = {}
    with open(unit_test_file, "r") as f:
        tests = f.readlines()
        no_of_tests = len(tests)
        passed_extraction = 0
        formatted_tests = []
        for i in range(no_of_tests):
            extraction_res, extraction_details = get_test_details(tests[i].strip())
            if extraction_res:
                passed_extraction += 1
                formatted_tests.append(extraction_details)

        if passed_extraction == no_of_tests:
            file_test_results["all_extracted"] = 1
            file_test_results["total_extracted"] = no_of_tests
            file_test_results["tests"] = formatted_tests
        f.close()
    
    return file_test_results

def generate_test_cases(source_file, source_lang, no_of_tests, model, is_unit_test=False, unit_test_file=None):
    # print(f"Generating tests for - {source_file}")
    code_id = Path(source_file).stem
    if code_id == "__pycache__" or Path(source_file).name.endswith(".class"):
        print(f"{source_file} is not a valid file to generate test cases")
        return None, None

    source_content = load_source_content(source_file)

    if not is_unit_test:
        content = source_content + f"\nGenerate {no_of_tests} test cases (only input) for the above {source_lang} code. Maintain the following format (x will be 0 to {no_of_tests - 1}):\nInput_0: <input>\nInput_1: <input>\n...\nInput_9: <input>\n//End Of Test\nDo not add any extra explanations or any other text except the mentioned output format."
        generated_test_cases = generate_test_cases_with_OPENAI(content, model)
        print("=" * 10, "Generated Test Cases", "=" * 10)
        print(generated_test_cases)
        print("=" * 10, "Generated Test Cases", "=" * 10)
        generated_test_cases = generated_test_cases.splitlines()
        return generated_test_cases, None
    
    if unit_test_file is None:
        print(f"Could not generate unit tests, provide sample unit test file for {source_file}")
        return None, None
    
    sample_unit_tests = extract_all_tests(unit_test_file)
    total_extracted = sample_unit_tests["total_extracted"]
    if total_extracted > 0:
        test_idx = 0
        sample_test_info = sample_unit_tests["tests"][test_idx]
        while(True):
            sample_test_info = sample_unit_tests["tests"][test_idx]
            if not ("''" in sample_test_info["func_input"] or "[]" in sample_test_info["func_input"] or "\"\"" in sample_test_info["func_input"]):
                break
            else:
                test_idx += 1

        test_name = sample_test_info["test_name"]
        func_name = sample_test_info["test_func"]
        func_input = sample_test_info["func_input"]
        sample_test = f"{test_name}: {func_name}({func_input})"

    content = source_content + f"\nGenerate {no_of_tests} inputs unit tests (only input) for the above {source_lang} code. For your reference a sample test case is as follow:\n{sample_test}. \nMaintain the following format (x will be 0 to {no_of_tests - 1}):\ntest_0: <test_case_0>\ntest_1: <test_case_1>\n...\ntest_x: <test_case_x>\n//End Of Test\nDo not add any extra explanations or any other text except the mentioned output format. Strictly follow the mentioned output format."
    generated_test_cases = generate_test_cases_with_OPENAI(content, model)
    generated_test_cases = generated_test_cases.splitlines()
    return generated_test_cases, sample_unit_tests

def run_files_to_generate_testfiles(source_file):
    code_id = Path(source_file).stem
    if code_id == "__pycache__" or code_id == "__init__" or code_id.endswith("temp") or Path(source_file).name.endswith(".class"):
        return
        
    Popen(['python3', source_file], cwd=os.getcwd(), stdin=PIPE, stdout=PIPE, stderr=PIPE)

def generate_test_extraction_ready_to_be_used(current_test_file):
    file_test_results = {}
    with open(current_test_file, "r") as f:
        temp_tests = f.readlines()
        test_start_idx = 0
        for j in range(len(temp_tests)):
            if temp_tests[j].strip() == "==================================================":
                test_start_idx = j + 1
                break
        tests = temp_tests[test_start_idx:]
        params = temp_tests[0:(test_start_idx-1)]
        params = [[param.strip().split(":", 1)[0].strip(), param.strip().split(":", 1)[1].strip()] for param in params]

        no_of_tests = len(tests)
        passed_extraction = 0
        formatted_tests = []
        for i in range(no_of_tests):
            extraction_res, extraction_details = get_test_details(tests[i].strip())
            if extraction_res:
                passed_extraction += 1
                formatted_tests.append(extraction_details)

        if passed_extraction == no_of_tests:
            file_test_results["params"] = params
            file_test_results["all_extracted"] = 1
            file_test_results["total_extracted"] = no_of_tests
            file_test_results["tests"] = formatted_tests
        f.close()
    
    return file_test_results

def separate_generated_test_cases(generated_test_cases):
    separated_test_cases = []
    current_input = ""
    for line in generated_test_cases:
        temp_line = re.sub(r'\binput\b', 'Input', line)
        if temp_line.startswith("Input_"):
            if current_input != "":
                separated_test_cases.append(current_input)
                current_input = ""
            
            current_input += temp_line + "\n"
        elif not temp_line.startswith("//End Of Test"):
            current_input += temp_line + "\n"
    
    if current_input != "":
        separated_test_cases.append(current_input)
    
    return separated_test_cases


def get_test_cases_with_oracle(source_file, no_of_tests, is_unit_test=False, unit_test_file=None, model = "gpt-4o-mini"):
    code_id = Path(source_file).stem
    if code_id == "__pycache__" or code_id == "__init__" or code_id.endswith("temp") or Path(source_file).name.endswith(".class"):
        return None, None
    source_lang_ext = str(Path(source_file).name).split(".")[-1]
    source_lang = ext_to_lang[source_lang_ext]
    generated_test_cases, sample_unit_tests = generate_test_cases(source_file, source_lang, no_of_tests, model, is_unit_test, unit_test_file)

    generated_test_cases = separate_generated_test_cases(generated_test_cases)

    temp_dir = f"{os.getcwd()}/temp_files/"
    os.makedirs(f"{os.getcwd()}/temp_files", exist_ok=True)

    if not is_unit_test:
        test_idx = 0
        generated_files = []
        # print("=" * 10, "Output Generation Failed", "=" * 10)
        for i in range(len(generated_test_cases)):
            temp_line = generated_test_cases[i].strip()
            temp_line = re.sub(r'\binput\b', 'Input', temp_line)
            if temp_line.startswith("Input_"):
                parts = temp_line.split(":")
                if len(parts) >= 3:
                    f_in = ""
                    for i in range(1, len(parts), 1):
                        f_in = f_in + parts[i] + ":"
                    f_in = f_in[:-1]
                elif len(parts) >= 2:
                    f_in = parts[1].strip()
                else:
                    continue
                f_in = f_in.replace(r'\n', '\n')
                verdict, f_out = Compiler.get_output(str(Path(source_file).parent), str(Path(source_file).name), f_in+"\n", source_lang)

                if verdict == Constants.OUTPUT_GENERATED:
                    with open(f"{temp_dir}{code_id}_{test_idx}.in", "w") as gen_inp_file:
                        gen_inp_file.write(f_in)
                        generated_files.append(f"{temp_dir}{code_id}_{test_idx}.in")
                        gen_inp_file.close()
                    with open(f"{temp_dir}{code_id}_{test_idx}.out", "w") as gen_out_file:
                        gen_out_file.write(f_out)
                        generated_files.append(f"{temp_dir}{code_id}_{test_idx}.out")
                        gen_out_file.close()
                    test_idx += 1
                # else:
                    # print(f"Input:\n{f_in}\nOutput:\n{f_out}")
            
        # print("=" * 10, "Output Generation Failed", "=" * 10)

        #remove all .class files generated
        dir_files = os.listdir(str(Path(source_file).parent))
        for file in dir_files:
            if ".class" in file: os.remove(str(Path(source_file).parent) +"/"+ file)

        dir_files = os.listdir(os.getcwd())
        for file in dir_files:
            if "exec_output" in file: os.remove(os.getcwd() +"/"+ file)

        return generated_files, None
        
    source_content = load_source_content(source_file)

    test_inputs = []
    test_names = []
    test_info = sample_unit_tests
    total_extracted = test_info["total_extracted"]

    if total_extracted > 0:
        test_idx = 0
        sample_test_info = test_info["tests"][test_idx]
        while(True):
            sample_test_info = test_info["tests"][test_idx]
            if not ("''" in sample_test_info["func_input"] or "[]" in sample_test_info["func_input"] or "\"\"" in sample_test_info["func_input"]):
                break
            else:
                test_idx += 1

    func_name = sample_test_info["test_func"]
    func_input = sample_test_info["func_input"]

    test_contents = generated_test_cases
    for temp_inp in test_contents:
        if temp_inp.startswith("test_"):
            line_parts = temp_inp.strip().split(":")
            test_name = line_parts[0]
            test_assertion = line_parts[1]
            if len(line_parts) > 2:
                for k in range(len(line_parts) - 2):
                    test_assertion = test_assertion + ":" + line_parts[k + 2]
            test_assertion = test_assertion.strip()
                    
            test_names.append(test_name)
            test_inputs.append(test_assertion)

    current_test_file = f"{temp_dir}get_oracle_{code_id}.py"

    # required code part to get entrypoint parameters
    f_content = "import inspect\n\ndef infer_return_type(func, *args):\n    result = func(*args)\n    if isinstance(result, list):\n        unique_types = {type(element).__name__ for element in result}\n        return f'list[{\", \".join(unique_types)}]'\n    elif isinstance(result, tuple):\n        unique_types = {type(element).__name__ for element in result}\n        return f'tuple({\", \".join(unique_types)})'\n    else:\n        return type(result).__name__\n\ndef get_function_parameters(func):\n    sig = inspect.signature(func)\n    params = list(sig.parameters.keys())\n    return params\n\ndef infer_types_at_runtime(func, *args):\n    param_names = get_function_parameters(func)\n    param_types = []\n\n    for name, arg in zip(param_names, args):\n        if isinstance(arg, list):\n            unique_types = {type(element).__name__ for element in arg}\n            param_types.append([name, f'list[{\", \".join(unique_types)}]'])\n        else:\n            param_types.append([name, type(arg).__name__])\n    return param_types\n\n"

    f_content = f_content + source_content + "\n" + "dir = \"" + temp_dir + code_id + ".txt\"\n" + "with open(dir, \"w\") as f:\n"

    f_content = f_content + "\n    inferred_types = infer_types_at_runtime(" + func_name + "," + func_input + ")\n    " + "for i in range(len(inferred_types)):\n        print(f\"{inferred_types[i][0]}: {inferred_types[i][1]}\", file=f)"

    f_content = f_content + "\n    ret_type = infer_return_type(" + func_name + "," + func_input + ")\n    print(f\"return: {ret_type}\", file=f)\n"

    f_content = f_content + "\n    print(\"==================================================\", file=f)\n"

    for j in range(len(test_inputs)):
        output_sentence = "    try:\n        output = " + test_inputs[j] + "\n        if type(output) == type(\"\"): output = \"\\\"\" + output + \"\\\"\" "
        input_sentence = "        input = \"" + test_inputs[j].replace("\"", "\\\"") + "\""
        f_content = f_content  + output_sentence + "\n" + input_sentence + "\n" + "        " + "print(f\"" + test_names[j] + ": self.assertEqual({output}, {input}" + ")\", file=f)\n" + "    except:\n        print(\"\")\n"

    f_content = f_content + "    f.close()\n"

    with open(current_test_file, "w") as f:
        print(f_content, file=f)
        f.close()

    run_files_to_generate_testfiles(current_test_file)

    if utility.wait_for_file(f"{temp_dir}{code_id}.txt", timeout=10):
        file_test_results = generate_test_extraction_ready_to_be_used(f"{temp_dir}{code_id}.txt")
        return [f"{temp_dir}{code_id}.txt"], file_test_results
        
    return None, None