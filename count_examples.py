import json

def count_examples(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    key = next(iter(data))

    with_examples = 0
    without_examples = 0

    for module in data.get(key, []):
        #module_name = module.get('module', 'Unknown module')
        qualified_name = module.get('qualified_name', 'Unknown qualified name')
        examples = module.get('examples', [])

        if examples:
            with_examples += 1
            #example_status = '😊'
        else:
            without_examples += 1
            #example_status = '😔'


        #print(f"{key}: {example_status}")
        if len(examples) > 0:
            print(f"{qualified_name}: {len(examples)} \n")

    total_modules = len(data.get(key, []))
    print(f"\nTotal {with_examples} modules have example out of {total_modules} modules.")


def main():
    file_path = 'documentations/help_emoji.json'
    count_examples(file_path)


if __name__ == "__main__":
    main()
