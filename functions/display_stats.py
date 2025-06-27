from tabulate import tabulate
import argparse

def display_stats_tabulate(data_dict, args):
    """
    Display summarized statistics of daily notes in a formatted table.

    Processes a dictionary of daily note data, extracting task completion stats,
    metadata, and word count, then prints a table with this information.
    Supports sorting by date or word count and limiting output to recent entries.

    Parameters:
        data_dict (dict): A dictionary where each key maps to an entry dict containing:
            - "date" (str): Date of the daily note.
            - "tasks" (list of dict): List of task dicts with "complete" (bool) key.
            - "metadata" (dict, optional): Additional key-value metadata.
            - "word_count" (int): Word count for the daily note.
        args (argparse.Namespace): Parsed command-line arguments with:
            - all (bool): If True, display all entries; else show last 5.
            - sort_wc (bool): If True, sort by word count; else by date.

    Prints:
        A formatted table summarizing each daily note's tasks, metadata, and word count.
    """
    table = [] 
    for entry_key, entry_data in data_dict.items():
        done = sum(task["complete"] for task in entry_data["tasks"])
        todo = len(entry_data["tasks"]) - done

        task_data = tabulate(
            [
            ["Total tasks:", len(entry_data["tasks"])],
            ["Complete / Incomplete:", f"{done} / {todo}"],
            ],
            tablefmt="plain",
            colalign=("left", "left")
            )
        
        metadata_list = []
        if "metadata" in entry_data:
            for metadata in entry_data["metadata"]:
                metadata_list.append([f"{metadata}:", (entry_data["metadata"][metadata])])
            metadata_data = tabulate(metadata_list, tablefmt="plain", colalign=("left", "left"))
        else:
            metadata_data = "No Metadata"

        table.append([entry_data["date"], task_data, metadata_data, entry_data["word_count"]])

    if args.sort_wc:
        # Word count sort
        table.sort(key=lambda row: row[3])
    else:
        #Default sort
        table.sort(key=lambda row: row[0])

    # flags=["--all"]
    if args.all:
        print(tabulate(table,  headers=["Daily Note", "Tasks", "Metadata", "Word Count"], tablefmt="grid"))
    else:
        # By default display last 5 entries
        print(tabulate(table[-5:],  headers=["Daily Note", "Tasks", "Metadata", "Word Count"], tablefmt="grid"))
