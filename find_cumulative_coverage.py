import xml.etree.ElementTree as ET

def parse_coverage_report(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # coverage_data = {}
    total_line_covered = 0
    total_lines = 0
    for file in root.findall(".//class"):
        filename = file.get('filename')
        for line in file.findall('lines/line'):
            total_lines += 1
            line_num = int(line.get('number'))
            hits = int(line.get('hits'))
            # coverage_data[str(line_num)] = {'missed': 1 if hits == 0 else 0, 'covered': hits}
            if hits != 0:
                total_line_covered += 1

    return total_line_covered / total_lines

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get cumulative coverage from a .xml coverage report")
    parser.add_argument("--xml", required=True, help="Path to xml file (coverage) with API metadata.")
    args = parser.parse_args()

    print(parse_coverage_report(args.xml))