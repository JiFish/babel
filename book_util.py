# DEVELOPER TOOL
# Splits or combines JSON files containing book data.

import os
import json
import argparse

def save_dicts_to_files(json_data, output_dir="lore_books"):
    """
    Splits a JSON list of dictionaries and saves each dictionary as a separate file.

    Parameters:
        json_data (str): Multi-line JSON list of dictionaries.
        output_dir (str): Directory to save the JSON files.
    """
    try:
        # Parse the input JSON data
        data = json.loads(json_data)

        if not isinstance(data, list):
            raise ValueError("Input JSON must be a list of dictionaries.")

        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        for item in data:
            if not isinstance(item, dict):
                raise ValueError("Each item in the JSON list must be a dictionary.")

            author = item.get("author", "Unknown Author")
            title = item.get("title", "Untitled")

            # Construct the filename
            filename = f"{author} - {title}.json".replace("/", "-").replace("\\", "-").replace("?", "")
            file_path = os.path.join(output_dir, filename)

            # Save the dictionary to a nicely formatted JSON file
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(item, file, indent=4, ensure_ascii=False)

        print(f"Successfully saved {len(data)} files to '{output_dir}'.")

    except json.JSONDecodeError:
        print("Invalid JSON data. Please check your input.")
    except Exception as e:
        print(f"An error occurred: {e}")


def combine_json_files(input_dir="lore_books", output_file="combined_books.json"):
    """
    Combines all JSON files in the specified directory into a single list,
    where each file is an entry in the list, and saves the result to disk.

    Args:
        input_dir (str): The path to the directory containing JSON files.
        output_file (str): The path to the output JSON file.
    """
    combined_data = []

    # Iterate over all files in the directory
    for filename in os.listdir(input_dir):
        # Build the full file path
        file_path = os.path.join(input_dir, filename)

        # Process only JSON files
        if os.path.isfile(file_path) and filename.endswith('.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    # Load JSON data and add it to the list
                    data = json.load(file)
                    combined_data.append(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON from {filename}: {e}")
            except Exception as e:
                print(f"Error processing {filename}: {e}")

    # Save the combined list to the output file
    try:
        with open(output_file, 'w', encoding='utf-8') as out_file:
            json.dump(combined_data, out_file, indent=4, ensure_ascii=False)
        print(f"Combined JSON saved to {output_file}")
    except Exception as e:
        print(f"Error saving to {output_file}: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split or combine JSON files."
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Subparser for splitting
    split_parser = subparsers.add_parser(
        "split",
        help="Split a JSON list into individual files.",
        description="Split a JSON list into individual files."
    )
    split_parser.add_argument("input_json", nargs="?", default="-", help="Path to the input JSON file or '-' for stdin (default: '-').")
    split_parser.add_argument("output_dir", nargs="?", default="lore_books", help="Directory to save the split JSON files (default: 'lore_books').")

    # Subparser for combining
    combine_parser = subparsers.add_parser(
        "combine",
        help="Combine individual JSON files into a single file.",
        description="Combine individual JSON files into a single file."
    )
    combine_parser.add_argument("input_dir", nargs="?", default="lore_books", help="Directory containing the JSON files to combine (default: 'lore_books').")
    combine_parser.add_argument("output_file", nargs="?", default="combined_books.json", help="Path to save the combined JSON file (default: 'combined_books.json').")

    args = parser.parse_args()

    if args.command == "split":
        if args.input_json == "-":
            print("Paste your multi-line JSON list of dictionaries below. Press Enter twice when done.")
            lines = []
            while True:
                line = input()
                if line.strip() == "":
                    break
                lines.append(line)
            json_input = "\n".join(lines)
        else:
            with open(args.input_json, "r", encoding="utf-8") as file:
                json_input = file.read()

        save_dicts_to_files(json_input, args.output_dir)

    elif args.command == "combine":
        combine_json_files(args.input_dir, args.output_file)

    else:
        parser.print_help()
