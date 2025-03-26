import importlib
import inspect
import pkgutil
import argparse
import os

def list_public_apis(package_name):
    try:
        package = importlib.import_module(package_name)
    except ModuleNotFoundError:
        print(f"Package '{package_name}' not found.")
        return {"functions": [], "classes": [], "methods": []}

    public_apis = {"functions": [], "classes": [], "methods": []}

    # Recursively explore all submodules
    def explore_module(module, module_name):
        for name, obj in inspect.getmembers(module):
            # Public functions
            if inspect.isfunction(obj) and not name.startswith("_"):
                public_apis["functions"].append((module_name, name, obj))  # Store function object

            # Public classes and their methods
            elif inspect.isclass(obj) and not name.startswith("_"):
                public_apis["classes"].append((module_name, name, obj))
                for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                    if not method_name.startswith("_"):
                        public_apis["methods"].append((module_name, name, method_name, method))

        if hasattr(module, "__path__"):  # Check if it’s a package with submodules
            for submodule_info in pkgutil.walk_packages(module.__path__, module_name + "."):
                try:
                    submodule = importlib.import_module(submodule_info.name)
                    explore_module(submodule, submodule_info.name)
                except Exception as e:
                    print(f"Skipping {submodule_info.name} due to error: {e}")

    explore_module(package, package_name)

    return public_apis

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List public APIs of a given Python package.")
    parser.add_argument("module_name", help="Name of the Python package to inspect.")
    args = parser.parse_args()

    public_apis = list_public_apis(args.module_name)

    documentation_dir = f"{os.getcwd()}/documentations"
    documentation_file = f"{documentation_dir}/help_{args.module_name}.txt"

    # saves a file in documentations folder with functions signatures and corresponding docstrings
    if public_apis is not [] or public_apis is not None:
        os.makedirs(documentation_dir, exist_ok=True)
        with open(documentation_file, "w") as f:
            for module_name, func_name, func_obj in public_apis["functions"]:
                try:
                    signature = inspect.signature(func_obj)  # Get function signature
                    docstring = inspect.getdoc(func_obj) or "⚠️ No documentation available."
                    print(f"\n{module_name}.{func_name}{signature}\n{'-'*len(func_name)}\n", file=f)
                    print(f"{docstring}\n", file=f)
                except Exception as e:
                    print(f"Skipping {module_name}.{func_name} due to error: {e}\n", file=f)
