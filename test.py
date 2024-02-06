import networkx as nx
import matplotlib.pyplot as plt

def create_graph(mainpid, nodes_and_dates):
    G = nx.Graph()

    # Add mainpid as a node
    G.add_node(mainpid, date='2001-09-16')

    # Add other nodes with their dates
    for pid, date in nodes_and_dates:
        G.add_node(pid, date=date)

    # Sort nodes by date in ascending order
    sorted_nodes = sorted(G.nodes(data=True), key=lambda x: x[1].get('date', ''))
    sorted_nodes = [node[0] for node in sorted_nodes]

    # Print sorted nodes
    print("Sorted nodes:")
    print(sorted_nodes)

    # Create a shell layout for mainpid and circular layout for other nodes
    shell_positions = nx.shell_layout(G, nlist=[[mainpid], sorted_nodes[1:]])
    circular_positions = nx.circular_layout(G)

    print(shell_positions)
    print(circular_positions)

    # Combine x and y coordinates for each node
    node_positions = {node: (shell_positions[node][0], circular_positions[node][1]) for node in sorted_nodes}

    # Add edges between mainpid and each node
    G.add_edges_from([(mainpid, node) for node in sorted_nodes[1:]])

    return G, node_positions

# Example usage:
mainpid = 'mainpid'
nodes_and_dates = [('pid1', '2022-01-01'), ('pid2', '2022-02-01'), ('pid3', '2022-03-01')]

graph, node_positions = create_graph(mainpid, nodes_and_dates)

# Draw the graph with manual positions
nx.draw(graph, pos=node_positions, with_labels=True, font_weight='bold', node_size=1000, node_color='skyblue', font_size=8)
plt.title("Graph with mainpid as source and sorted targets based on ascending date (no overlap)")
plt.show()