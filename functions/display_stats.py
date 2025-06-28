from tabulate import tabulate
import shutil
import math

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
    # else: default or --count flag
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
        #Default sort
        table.sort(key=lambda row: row[0])
    
    # Display the table
    print(tabulate(table,  headers=["Daily Note", "Tasks", "Metadata", "Word Count"], tablefmt="grid"))


def display_wc_graph(data_dict, args):
    # Build data set to be displayed **function**
    data_set = build_data_set(data_dict, args)

    # Calculate graphing boundaries **graphing**
    columns, _ = shutil.get_terminal_size()
    columns = min(columns, 100)
    max_title_len = max(len(data_set[k]["date"]) for k in data_set)
    max_value_len = max(data_set[k]["word_count"] for k in data_set)
    max_bar_len = (columns - max_title_len - len(str(max_value_len))) - 4 
    data_normalisation_factor = float(max_bar_len - 1) / max_value_len

    # Build table of data to be graphed **function**
    row_data = []
    for entry_key, entry_data in data_set.items():
        bar_len = max(0, math.floor(entry_data["word_count"] * data_normalisation_factor))
        row_data.append([entry_data["date"], bar_len, entry_data["word_count"]])
    
    # Generate rows from data to be graphed **graphing**
    rows = []
    for item in row_data:
        if item[2] <= 0:
        # For values 0 or less show only legend
            rows.append(f"{item[0]}: ")
        elif item[1] <= 0:
        # For bar values of 0 but data is above zero, bar size 1
            rows.append(f"{item[0]}: ⬢ {item[2]}")
        else:
        # Normal operation, display scaled bar and data
            bar = item[1] * "⬢"
            rows.append(f"{item[0]}: {bar} {item[2]}")

    # Print graph title **graphing**
    title = "#### Graph of word counts "
    justified_title = title.ljust(columns, "#")
    print("\n" + "#" * columns)
    print(f"{justified_title}")
    print("#" * columns + "\n")

    # Print each row to the terminal **graphing**
    for string in rows:
        print(string)
    print("\n" + "#" * columns)
    print(f"#" * columns + "\n")