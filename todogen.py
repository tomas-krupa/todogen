#!/usr/bin/env python3

import os
import re
import argparse

# Define the TODO section header
TODO_SECTION_HEADER = "## TODOs\n"


def find_todos_in_files(root_dir, extensions=None):
    """
    Traverse files in the given directory and find TODO comments.
    :param root_dir: Root directory to search.
    :param extensions: List of file extensions to include, or None for all.
    :return: List of TODO strings.
    """
    todos = []
    todo_pattern = re.compile(
        r"(//\s*TODO[:\s]*(.+)|/\*\s*TODO[:\s]*([^\*/]+)\*/)", re.IGNORECASE
    )
    extensions = extensions or []

    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if extensions and not file.endswith(tuple(extensions)):
                continue
            filepath = os.path.join(subdir, file)
            try:
                # Get the relative path from root_dir to the file
                relative_filepath = os.path.relpath(filepath, root_dir)

                with open(filepath, "r", encoding="utf-8") as f:
                    for line_no, line in enumerate(f, start=1):
                        match = todo_pattern.search(line)
                        if match:
                            # Generate the relative link to source code
                            relative_filepath_normalized = relative_filepath.replace(
                                "\\", "/"
                            )
                            file_link = f"[{relative_filepath}:{line_no}]({relative_filepath_normalized}#L{line_no})"
                            todos.append(f"{file_link} - {match.group(1).strip()}")
            except Exception as e:
                print(f"Error reading file {filepath}: {e}")

    return todos


def append_todos_to_readme(readme_file, todos):
    """
    Append TODOs to the README file.
    :param readme_file: Path to README file.
    :param todos: List of TODO strings.
    """
    if not todos:
        print("No TODOs found.")
        return

    try:
        with open(readme_file, "r", encoding="utf-8") as f:
            content = f.read()

        if TODO_SECTION_HEADER in content:
            # Remove old TODO section
            content = content.split(TODO_SECTION_HEADER, 1)[0]
            content += TODO_SECTION_HEADER
        else:
            content += "\n" + TODO_SECTION_HEADER
        # Append updated TODOs
        content += "\n".join(f"- {todo}" for todo in todos) + "\n"

        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"TODOs appended to {os.path.basename(readme_file)}.")
    except FileNotFoundError:
        print(f"{readme_file} not found. Creating a new one.")
        with open(readme_file, "w", encoding="utf-8") as f:
            f.write(TODO_SECTION_HEADER)
            f.writelines(f"- {todo}\n" for todo in todos)
    except Exception as e:
        print(f"Error updating {readme_file}: {e}")


def parse_arguments():
    """
    Parse command-line arguments.
    :return: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Find TODO comments in code files and append them to a README file."
    )
    parser.add_argument("--readme", type=str, help="Path to the README.md file.")
    parser.add_argument(
        "--src", type=str, help="Root source directory of code files to search."
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    # Extensions to search (add more as needed)
    file_extensions = ["*.txt", ".qml", ".cpp", ".h", ".java", ".kt"]
    todos = find_todos_in_files(args.src, file_extensions)
    append_todos_to_readme(args.readme, todos)
