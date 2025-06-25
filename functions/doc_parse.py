import os
import re
import yaml
from CONFIG import *

def parse_md_files(path, data_dict, base_path):
    """
    Recursively parses markdown (.md) files from a directory tree.

    For each markdown file found:
    - Reads its contents and stores it in `data_dict` under its relative path.
    - Skips hidden files and directories (starting with '.').
    - Relative paths are calculated from the `base_path`.

    Args:
        path (str): Current directory path to scan.
        data_dict (dict): Dictionary to store file contents.
                          Keys are relative paths, values are dicts with a 'content' key.
        base_path (str): Root directory used to compute relative paths.
    """
    for item in os.listdir(path):
        if item.startswith("."):
            continue
        item_abs_path = os.path.join(path, item)
        rel_path = os.path.relpath(item_abs_path, start=base_path)
        if os.path.isfile(item_abs_path):
            if item_abs_path.endswith(".md"):
                try:
                    with open(item_abs_path, "r", encoding="utf-8") as f:
                        data_dict[rel_path] = {}
                        data_dict[rel_path]["content"] = f.read()
                except Exception as e:
                    print(f"Exception: {e}")
                    print(f"Error reading file {rel_path}")
                    continue
        else:
            #print(f"{item} is a directory...")
            parse_md_files(item_abs_path, data_dict, base_path)

def extract_metadata(data_dict):
    """
    Extracts YAML frontmatter metadata from markdown content in `data_dict`.

    For each entry:
    - If frontmatter is found, it is parsed and stored under 'metadata'.
    - The remaining content (without frontmatter) is stored as 'content_no_yaml'.
    - If no frontmatter exists, the full content is stored as 'content_no_yaml'.

    Args:
        data_dict (dict): Dictionary with markdown content under each key.
                          Each value must contain a 'content' key with the raw file content.
    """
    FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
    for key in data_dict:
        content = data_dict[key]["content"]
        data_dict[key]["content_no_yaml"] = content
        if content.startswith("---\n"):
            match = re.match(FRONTMATTER_RE, content)
            data_dict[key]["content_no_yaml"] = re.sub(FRONTMATTER_RE,"", content).lstrip()
            if not match:
                print("no match")
                continue
            raw_metadata = match.group(1)
            try:
                data_dict[key]["metadata"] = yaml.safe_load(raw_metadata)
            except yaml.YAMLError as e:
                print(f"YAML parse error in {key}: {e}")

def extract_tasks(data_dict):
    """
    Extracts top-level tasks from markdown content in `data_dict`.

    Tasks are expected to be in the form:
        - [ ] task description
        - [x] completed task
        - [*] alternate state (also treated as incomplete)

    Only top-level tasks (no leading indentation) are matched.
    Extracted tasks are stored as a list of dicts under the 'tasks' key.

    Args:
        data_dict (dict): Dictionary with 'content_no_yaml' per entry (stripped of frontmatter).
    """
    ANY_TASK_RE = re.compile(r'^[ \t]*- \[(.)\](.*)')
    TOP_LEVEL_TASK_RE = re.compile(r'^[ ]{0,3}- \[(.)\](.*)')
    for key in data_dict:
        data_dict[key]["tasks"] = []
        if "content_no_yaml" not in data_dict[key]:
            continue
        content = data_dict[key].get("content_no_yaml")
        if not content:
            continue
        lines = content.splitlines()
        for item in lines:
            match = TOP_LEVEL_TASK_RE.match(item)
            if match:
                complete = match.group(1).lower() == "x"
                data_dict[key]["tasks"].append({"complete": complete, "task": match.group(2).strip()})
        #print(f"\nExtracted tasks from {key}:\n--------\n{repr(data_dict[key]['tasks'])}\n--------\n")
        
def extract_wordcount(data_dict):
    """
    Calculate the effective word count for each file in data_dict,
    excluding a fixed number of words defined in TEMPLATE_WORD_COUNT
    (e.g. from a static frontmatter template).

    Sets 'word_count' to 0 if the adjusted count is negative.
    """
    for key in data_dict:
        word_list = re.findall(r'\b\w+\b', data_dict[key]["content"])
        data_dict[key]["word_count"] = max(0, len(word_list) - TEMPLATE_WORD_COUNT)
        #print(f"\nWord count of {key}: {data_dict[key]['word_count']}")