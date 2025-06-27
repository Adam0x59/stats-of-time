from tabulate import tabulate

def display_stats_tabulate(data_dict, flags=None):
    table = [] 
    for key in data_dict:
        done = 0
        todo = 0
        for task in data_dict[key]["tasks"]:
            if task["complete"]:
                done +=1
            else:
                todo +=1

        task_data = tabulate(
            [
            ["Total tasks:", len(data_dict[key]["tasks"])],
            ["Complete/Incomplete:", f"{done}/{todo}"],
            ],
            tablefmt="plain",
            colalign=("left", "left")
            )
        
        metadata_list = []
        for metadata in data_dict[key]["metadata"]:
            metadata_list.append([f"{metadata}:", (data_dict[key]["metadata"][metadata])])
        
        metadata_data = tabulate(metadata_list, tablefmt="plain", colalign=("left", "left"))
        
        table.append([data_dict[key]["date"], task_data, metadata_data, data_dict[key]["word_count"]])
        table.sort(key=lambda row: row[0])
    
    print(tabulate(table, headers=["Daily Note", "Tasks", "Metadata", "Word Count"], tablefmt="grid"))