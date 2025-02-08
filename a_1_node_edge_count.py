import networkit as nk

def main():

    # Define file paths
    csv_file = "open_citations_curated.csv"  # Update with your actual file path
    output_file = "node_edge_count.txt"  # File to store results

    # Initialize a directed graph
    graph = nk.graph.Graph(directed=True)

    # Dictionary to map node labels to unique indices
    node_map = {}
    node_counter = 0  # Counter to assign unique node indices

    # Read the CSV file line by line
    with open(csv_file, "r") as file:
        # Read the header and determine column indices
        header = file.readline().strip().split(",")
        citing_index = header.index("citing")  # Find index of 'citing'
        cited_index = header.index("cited")  # Find index of 'cited'

        for line in file:
            row = line.strip().split(",")
            if len(row) < 2:  # Skip invalid lines
                continue

            u, v = row[citing_index], row[cited_index]

            # Assign unique indices if not already mapped
            if u not in node_map:
                node_map[u] = node_counter
                graph.addNode()
                node_counter += 1
            if v not in node_map:
                node_map[v] = node_counter
                graph.addNode()
                node_counter += 1

            # Add edge
            graph.addEdge(node_map[u], node_map[v])

    # Get number of nodes and edges
    num_nodes = graph.numberOfNodes()
    num_edges = graph.numberOfEdges()

    # Write to output file
    with open(output_file, "w") as f:
        f.write(f"Number of nodes: {num_nodes}\n")
        f.write(f"Number of edges: {num_edges}\n")

    print(f"Results saved to {output_file}")


if __name__ == "__main__":
    main()
