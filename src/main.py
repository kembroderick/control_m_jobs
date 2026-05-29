import argparse
import sys
from .parser import parse_excel
from .generator import generate_json


def main():
    parser = argparse.ArgumentParser(description="Convert Excel job definitions to Control-M JSON")
    parser.add_argument("input", help="Path to the Excel file")
    parser.add_argument("-o", "--output", help="Output file path (default: stdout)")
    args = parser.parse_args()

    jobs = parse_excel(args.input)
    result = generate_json(jobs)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
        print(f"Written to {args.output}")
    else:
        sys.stdout.write(result + "\n")


if __name__ == "__main__":
    main()
