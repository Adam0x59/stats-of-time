from CONFIG import *
import os
import sys
import argparse
from functions.doc_parse import *
from functions.display_stats import *

def process_vault(path):
    data_dict = {}
    parse_md_files(path, data_dict, base_path=path)
    extract_date(data_dict)
    extract_metadata(data_dict)
    extract_tasks(data_dict)
    extract_wordcount(data_dict)
    return data_dict

def main():

    parser = argparse.ArgumentParser(description="Parse and display stats from Obsidian markdown vault")
    parser.add_argument('-a','--all', action='store_true', help='List all data - Default is most recent 5 rows')
    parser.add_argument('-c', '--count', type=int, default=5, help='List data for "COUNT" number of results from the most recent entry back')
    parser.add_argument('-g', '--graph', action='store_true', help='Enable graph mode')
    parser.add_argument('-s', '--sort_wc', action='store_true', help='Sort by word count')
    parser.add_argument('-G', '--graph-only', action='store_true', help='Only display graphs')
    args = parser.parse_args()

    # Identify and parse .md files from directories in OBSIDIAN_VAULT_PATH
    # recursively and store content in data_dict to await further processing
    directory_path = os.path.abspath(os.path.expanduser(OBSIDIAN_VAULT_PATH))
    #print(f"Resolved path: {directory_path}")
    if not os.path.exists(directory_path):
        print("Provided path does not exist - exiting program!")
        sys.exit(1)
    
    data_dict = process_vault(directory_path) 

    # Display stats in a tablulate table within the shell
    if not args.graph_only:
        display_stats_tabulate(data_dict, args)
        if args.graph:
            display_wc_graph(data_dict, args)
    else:
        display_wc_graph(data_dict, args)

    '''
    for key in data_dict:
        print("############################################################")
        for sub_key in data_dict[key]:
            print(f"\n{sub_key}:\n----\n{data_dict[key][sub_key]}\n----\n")
        print("############################################################\n")
    '''
        
if __name__ == "__main__":
    main()