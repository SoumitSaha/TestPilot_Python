import importlib
import inspect
import pkgutil
import argparse
import os
import json

def list_public_apis(package_name):
    try:
        package = importlib.import_module(package_name)
    except ModuleNotFoundError:
        print(f"Package '{package_name}' not found.")
        return {"functions": [], "classes": [], "methods": []}

    public_apis = {"functions": [], "classes": [], "methods": []}

    def explore_module(module, module_name):
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) and not name.startswith("_"):
                public_apis["functions"].append((module_name, name, obj))
            elif inspect.isclass(obj) and not name.startswith("_"):
                public_apis["classes"].append((module_name, name, obj))
                for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                    if not method_name.startswith("_"):
                        public_apis["methods"].append((module_name, name, method_name, method))

        if hasattr(module, "__path__"):  # Check if it’s a package with submodules
        if hasattr(module, "__path__"):
            for submodule_info in pkgutil.walk_packages(module.__path__, module_name + "."):
                try:
                    submodule = importlib.import_module(submodule_info.name)
                    explore_module(submodule, submodule_info.name)
                except Exception as e:
                    print(f"Skipping {submodule_info.name} due to error: {e}")

    explore_module(package, package_name)
    return public_apis

def extract_public_api_json(package_name):
    apis = list_public_apis(package_name)
    results = {package_name: []}

    def get_parameters(sig):
        return {
            name: {
                "default": str(param.default) if param.default is not param.empty else None,
                "annotation": str(param.annotation) if param.annotation is not param.empty else None,
                "kind": str(param.kind)
            }
            for name, param in sig.parameters.items()
        }

    for module, name, obj in apis["functions"]:
        try:
            sig = inspect.signature(obj)
            results[package_name].append({
                "type": "function",
                "qualified_name": f"{module}.{name}",
                "module": module,
                "signature": str(sig),
                "parameters": get_parameters(sig),
                "returns": str(sig.return_annotation) if sig.return_annotation is not inspect.Signature.empty else None,
                "docstring": inspect.getdoc(obj) or ""
            })
        except Exception:
            continue

    for module, class_name, cls in apis["classes"]:
        try:
            init_sig = inspect.signature(cls.__init__) if hasattr(cls, "__init__") else None
            results[package_name].append({
                "type": "class",
                "qualified_name": f"{module}.{class_name}",
                "module": module,
                "signature": str(init_sig) if init_sig else None,
                "docstring": inspect.getdoc(cls) or ""
            })
        except Exception:
            continue

    for module, class_name, method_name, method in apis["methods"]:
        try:
            sig = inspect.signature(method)
            results[package_name].append({
                "type": "method",
                "qualified_name": f"{module}.{class_name}.{method_name}",
                "module": module,
                "signature": str(sig),
                "parameters": get_parameters(sig),
                "returns": str(sig.return_annotation) if sig.return_annotation is not inspect.Signature.empty else None,
                "docstring": inspect.getdoc(method) or ""
            })
        except Exception:
            continue

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List public APIs of a given Python package.")
    parser.add_argument("module_name", help="Name of the Python package to inspect.")
    parser.add_argument("--json", action="store_true", help="Also export as JSON.")
    args = parser.parse_args()

    public_apis = list_public_apis(args.module_name)
    documentation_dir = f"{os.getcwd()}/documentations"
    os.makedirs(documentation_dir, exist_ok=True)
    documentation_file = f"{documentation_dir}/help_{args.module_name}.txt"

    if public_apis:
        with open(documentation_file, "w") as f:
            for module_name, func_name, func_obj in public_apis["functions"]:
                try:
                    signature = inspect.signature(func_obj)
                    docstring = inspect.getdoc(func_obj) or "⚠️ No documentation available."
                    print(f"\n{module_name}.{func_name}{signature}\n{'-'*len(func_name)}\n", file=f)
                    print(f"{docstring}\n", file=f)
                except Exception as e:
                    print(f"Skipping {module_name}.{func_name} due to error: {e}\n", file=f)

    if args.json:
        json_data = extract_public_api_json(args.module_name)
        json_file = f"{documentation_dir}/help_{args.module_name}.json"
        with open(json_file, "w") as jf:
            json.dump(json_data, jf, indent=2)