# Mapping_tools

## Data Preparation:
- The `pid_title_date.json` file is created by extracting the title and date information for each paper from its metadata.
- The extracted information is stored in the JSON format with the paper's PID as the key and its title and date as values.

## Null Date Removal:
After generating `pid_title_date.json`, `remove_null.py` script replaces null dates with those from `Cit-HepTh-dates.txt` for accurate analysis and visualization.

## Functions:
- `get_pids_from_title(json_file, title)`: Retrieves paper IDs (PIDs) from a JSON file based on the provided title.
- `extract_node2_from_link_file(link_file_path, pid)`: Extracts node2 PIDs from a text file containing citation links, given a node1 PID.
- `get_date_for_pid(json_file, pid)`: Retrieves the publication date of a paper from a JSON file based on its PID.
- `create_graph(mainpid, nodes_and_dates, jsontitle_file)`: Constructs a graph using NetworkX, with the main paper PID as the source node and other papers as target nodes. Sorts nodes by publication date and assigns layout positions for visualization.

## Usage:
The script prompts the user to input the title of a paper.
It retrieves relevant PIDs based on the title and extracts citation information.
Using NetworkX, it constructs a graph of paper citations and visualizes it using Matplotlib.

## Dependency:
- Python 3.x
- NetworkX
- Matplotlib
