from tabulate import tabulate
from functions.graph import *

def build_data_set(data_dict, args):
    """
    Build the filtered and sorted data set based on command-line arguments.
    
    Args:
        data_dict (dict): Original full data dictionary.
        args (argparse.Namespace): Parsed arguments (expects .all and .count)
        
    Returns:
        dict: Filtered and sorted data set to display.
    """
    # --all flag: show everything, keep sorted by date
    if args.all:
        data_list = list(data_dict.items())
        data_list.sort(key=lambda item: item[1]["date"])
        return dict(data_list)
    # default or --count flag
    data_list = sorted(data_dict.items(), key=lambda item: item[1]["date"])
    # Take the last N entries (args.count)
    selected_items = data_list[-args.count:]
    return dict(selected_items)
    

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
    data_set = build_data_set(data_dict, args)
    for entry_key, entry_data in data_set.items():
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
        #Default sort (date)
        table.sort(key=lambda row: row[0])
    
    # Display the table
    print(tabulate(table,  headers=["Daily Note", "Tasks", "Metadata", "Word Count"], tablefmt="grid"))


def display_wc_graph(data_dict, args):
    """
    Build and display a horizontal bar graph of word counts from the given data.

    Args:
        data_dict: dict, containing data records keyed by identifier (e.g., dates)
        args: object or dict, parameters or filters to be used by build_data_set

    Workflow:
        - Calls build_data_set() to prepare the filtered/processed data.
        - Extracts date and word count from each entry to build a data list.
        - Passes this list to bar_graph() to render the graph in terminal.
    """
    # Build data set to be displayed
    data_set = build_data_set(data_dict, args)
    # Generate data list for graphing function
    data = []
    for key, key_data in data_set.items():
        data.append([key_data["date"], key_data["word_count"]])
    title = "Graph of word counts"
    # Call graphing function
    bar_graph(data, title)
