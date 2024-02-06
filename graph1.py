import random
import json


import networkx as nx
import sys
# import networkx as nx
import matplotlib.pyplot as plt

def get_pids_from_title(json_file, title):
    matching_pids = []

    with open(json_file, 'r', encoding='utf-8') as file:
        paper_data = json.load(file)

    for pid, data in paper_data.items():
        if 'title' in data and data['title'].lower() == title.lower():
            matching_pids.append(pid)

    return matching_pids

def extract_node2_from_link_file(link_file_path, pid):
    with open(link_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    node2_list = []

    for line in lines:
        node1, node2 = line.strip().split()
        if node1 == pid:
            node2_list.append(node2)

    return node2_list

def get_date_for_pid(json_file, pid):
    with open(json_file, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None

    for stored_pid, info in data.items():
        if stored_pid.strip() == pid.strip():
            date = info.get("date")
            if date in [None, ""]:
                return None
            return date

    return None
def create_graph(mainpid, nodes_and_dates, jsontitle_file):
    G = nx.Graph()

    # Add mainpid as a node
    G.add_node(mainpid, date=get_date_for_pid(jsontitle_file, mainpid))

    # Add other nodes with their dates
    for pid, date in nodes_and_dates:
        G.add_node(pid, date=date)

    # Sort nodes by date in ascending order
    sorted_nodes = sorted(G.nodes(data=True), key=lambda x: x[1].get('date', ''))
    sorted_nodes = [node[0] for node in sorted_nodes]

    # Print sorted nodes and associated dates
    print("Sorted nodes:")
    print(sorted_nodes)
    print("Node dates:")
    for node in sorted_nodes:
        print(f"{node}: {G.nodes[node]['date']}")

    # Create a shell layout for mainpid and circular layout for other nodes
    shell_positions = nx.shell_layout(G, nlist=[[mainpid], [node for node in sorted_nodes if node != mainpid]])
    circular_positions = nx.circular_layout(G)

    # Print the layout positions
    print("Shell positions:")
    print(shell_positions)
    print("Circular positions:")
    print(circular_positions)

    # Combine x and y coordinates for each node
    node_positions = {node: (shell_positions[node][0], circular_positions[node][1]) for node in sorted_nodes}

    # Add edges between mainpid and each node
    G.add_edges_from([(mainpid, node) for node in sorted_nodes if node!=mainpid])

    return G, node_positions


# app = dash.Dash(__name__)

# Get user input for the paper title
user_input = input("Enter the title of the paper: ")

# Path to metadata directory
meta_directory = "./cit-HepTh-abstracts"

jsontitle_file = 'pid_title_date.json'

listofpids = get_pids_from_title(jsontitle_file, user_input)

pid = 0
if len(listofpids) == 0:
    print("Title didn't match. No paper found.")
    sys.exit(1)
elif len(listofpids) > 1:
    print(listofpids,)
    ind = int(input("Which pid you want to see.. enter the index:"))
    pid = listofpids[ind]
else:
    pid = listofpids[0]

jsonindex_file = 'pid_index.json'
link_file_path = "cit-HepTh.txt/Cit-HepTh.txt"

node2_list = extract_node2_from_link_file(link_file_path, pid)
print(node2_list)

time_file_path = './cit-HepTh-dates.txt/Cit-HepTh-dates.txt'

nodesanddates = []

for node2_pid in node2_list:
    date = get_date_for_pid(jsontitle_file, node2_pid)
    if date is None or date == "":
        date = "2024-02-01"
    
    nodesanddates.append((node2_pid, date))
print(nodesanddates)
mainpid = pid
# nodesanddates.append((mainpid, get_date_for_pid(jsontitle_file, mainpid)))
nodesanddates = sorted(nodesanddates, key=lambda x: x[1])
# print(nodesanddates)

# Create a networkx graph
graph, node_positions = create_graph(mainpid, nodesanddates,jsontitle_file)

# Draw the graph with manual positions
nx.draw(graph, pos=node_positions, with_labels=True, font_weight='bold', node_size=1000, node_color='skyblue', font_size=8)
plt.title("Graph with mainpid as source and sorted targets based on ascending date (no overlap)")
plt.show()

