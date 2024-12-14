from pathlib import Path

def add_more_in_md_files(directory):
    """
    Check all .md files in the specified directory.
    If <!-- more --> is not found, insert it between lines 15~30,
    prioritizing before ## or ### headers.
    """
    directory_path = Path(directory)

    # Iterate through all .md files in the directory and subdirectories
    for md_file in directory_path.rglob("*.md"):
        with md_file.open("r", encoding="utf-8") as file:
            lines = file.readlines()

        # Skip files that already contain <!-- more -->
        if any("<!-- more -->" in line for line in lines):
            print(f"File already contains <!-- more -->: {md_file}")
            continue

        # Search for the first ## or ### header between lines 15 and 30
        insert_index = None
        for i in range(14, min(len(lines), 30)):  # Line indices start at 0
            if lines[i].strip().startswith(("##", "###")):
                insert_index = i
                break

        # If no suitable header is found, default to inserting at line 15
        if insert_index is None:
            insert_index = min(14, len(lines) - 1)  # Ensure the index is valid

        # Insert <!-- more --> at the determined position
        lines.insert(insert_index, "<!-- more -->\n")

        # Write the updated content back to the file
        with md_file.open("w", encoding="utf-8") as file:
            file.writelines(lines)

        print(f"Inserted <!-- more --> into file: {md_file} at line {insert_index + 1}")

# Example usage
if __name__ == "__main__":
    directory_to_check = "./source/_posts"  # Replace with the target directory path
    add_more_in_md_files(directory_to_check)
