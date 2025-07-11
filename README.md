# stats-of-time

A CLI application written in python, to provide stats derived from .md files (Obsidian daily notes; this is what I use, It's my program, It does what I want it to do... Mostly...) 

## How it works
- Parses Markdown files - Uses the file-name as the date for sorting - YYYY-MM-DD format (Or defaults to when the file was created, but you're using daily notes, RIGHT?!)
    - Grab any metadata stored in the frontmatter YAML, Eg:
    ```
    ---
    Excercise: 50
    Code-Mins: 60
    Breakfast: true
    Lunch: false
    Dinner: true
    ---
    ```
    - Grab any top-level tasks, the following would be (Total tasks: 4, Complete/Incomplete: 2/2):
    ```
    - [x] Buy food
    - [/] Eat food
        - [x] Lunch
        - [x] Diner
    - [x] Read a chapter of some book
    - [ ] Write the readme for stats-of-time
    ```
    - Perform a word-count, less your template length (as defined in CONFIG.py)

- Displays the stats:
    - By default it displays the 5 latest entries (sorted by file-name date), in a Tabulate table, in the terminal.
    - If option `./run.sh -c <count>` is specified Eg: `./run.sh -c 10` the latest 10 results will be displayed.
    - If option `./run.sh -g` is specified a bar graph of each file's word count will be displayed.
    - Option `./run.sh -G` will only display the bar Graph.
