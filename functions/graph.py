import math
import shutil

def bar_graph(data, title, max_width=100, symbol="⬢", show_values=True):
    """
    Render a horizontal bar graph in terminal.

    Args:
        data: list of lists [[row_legend, row value], ...]
        title: str, title of graph
        --- Optional ---
        max_width: int, maximum width of the graph including labels
        symbol: str, character used to draw the bars
        show_values: bool, whether to display numeric values next to bars
    """
    columns, scaled_data = normalise_bar_graph_data(data, max_width)
    rows = generate_bar_graph_rows(scaled_data, symbol, show_values)
    print_bar_graph(title, columns, rows)


def normalise_bar_graph_data(data, max_width):
    """
    Normalize and scale data values to fit within a terminal-based horizontal bar graph.

    Args:
        data: list of lists [[label, value], ...]
        max_width: int, maximum width of the graph including labels and numbers

    Returns:
        tuple: (columns, scaled_data)
            - columns: int, actual terminal width used
            - scaled_data: list of lists [[label, value, scaled_bar_length], ...]
    """
    columns, _ = shutil.get_terminal_size()
    columns = min(columns, max_width)
    max_title_len = max(len(item[0]) for item in data)
    max_value_len = max(item[1] for item in data)
    max_bar_len = (columns - max_title_len - len(str(max_value_len))) - 3 
    data_normalisation_factor = float(max_bar_len - 1) / max_value_len
    # Calc bar_len for data items and populate new list
    scaled_data = []
    for item in data:
        scaled_data.append([item[0], item[1], max(0, math.floor(item[1] * data_normalisation_factor))])
    return columns, scaled_data

def generate_bar_graph_rows(data, symbol, show_values):
    """
    Create text rows for each item to be displayed in the bar graph.

    Args:
        data: list of lists [[label, value, scaled_bar_length], ...]
        symbol: str, character to use for the bars
        show_values: bool, whether to append the numeric value after each bar

    Returns:
        list of strings, each representing a formatted line of the graph
    """
    rows = []
    for item in data:
        if item[1] <= 0:
        # For values 0 or less show only legend
            rows.append(f"{item[0]}: ")
        elif item[2] <= 0:
        # For bar values of 0 but data is above zero, bar size 1
            rows.append(f"{item[0]}: {symbol}" + (f" {item[1]}" if show_values else ""))
        else:
        # Normal operation, display scaled bar and data
            bar = item[2] * symbol
            rows.append(f"{item[0]}: {bar}" + (f" {item[1]}" if show_values else ""))
    return rows

def print_bar_graph(title, columns, rows):
    """
    Print the complete horizontal bar graph to the terminal, including title and borders.

    Args:
        title: str, title to display above the graph
        columns: int, width of the graph in characters
        rows: list of strings, the formatted lines representing the graph bars
    """
    # Print title
    title = "#### " + title + " "
    justified_title = title.ljust(columns, "#")
    print("\n" + "#" * columns)
    print(f"{justified_title}")
    print("#" * columns + "\n")
    # Print rows
    for string in rows:
        print(string)
    print("\n" + "#" * columns)
    print(f"#" * columns + "\n")