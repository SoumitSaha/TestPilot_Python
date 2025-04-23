import xml.etree.ElementTree as ET

def parse_coverage_report(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    total_loc = 0
    for line in root.findall(".//line"):
        total_loc += 1

    total_line_rate = 0
    total_branch_rate = 0
    total_packages = 0

    min_coverage = 100
    max_coverage = 0

    for package in root.findall(".//package"):
        line_rate = float(package.get('line-rate', 0))
        if line_rate > max_coverage:
            max_coverage = line_rate
        
        if line_rate < min_coverage:
            min_coverage = line_rate

        branch_rate = float(package.get('branch-rate', 0))

        total_line_rate += line_rate
        total_branch_rate += branch_rate
        total_packages += 1

    # Calculate averages
    avg_line_rate = total_line_rate / total_packages if total_packages > 0 else 0
    avg_branch_rate = total_branch_rate / total_packages if total_packages > 0 else 0

    return avg_line_rate, min_coverage, max_coverage, avg_branch_rate, total_packages, total_loc

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Get cumulative coverage from a .xml coverage report")
    parser.add_argument("--xml", required=True, help="Path to xml file (coverage) with API metadata.")
    args = parser.parse_args()

    avg_line_rate, min_coverage, max_coverage, avg_branch_rate, total_packages, total_loc = parse_coverage_report(args.xml)
    print(f"Average Line Coverage: {avg_line_rate * 100:.2f}%")
    print(f"Average Branch Coverage: {avg_branch_rate * 100:.2f}%")
    print(f"Min Line Coverage: {min_coverage * 100:.2f}%")
    print(f"Max Line Coverage: {max_coverage * 100:.2f}%")
    print(f"Total Modules: {total_packages}")
    print(f"Total Modules: {total_loc}")
    