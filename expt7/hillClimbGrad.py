def simple_hill_climbing(graph, start, heuristic_values):
    current = start
    path = [current]
    while True:
        neighbors = graph.get(current, [])
        next_node = None
        for neighbor in neighbors:
            if neighbor in heuristic_values and heuristic_values[neighbor] < heuristic_values[current]:
                next_node = neighbor
                break
        if next_node is None:
            break            
        current = next_node
        path.append(current)
    return path
if __name__ == "__main__":
    graph = {}
    heuristic_values = {}
    print("Enter node, neighbours, heuristic value:")
    while True:
        line = input().strip()
        if not line: break
        parts = [p.strip() for p in line.split(',')]
        node_name = parts[0]
        neighbors_list = parts[1].split()
        h_value = int(parts[2])
        graph[node_name] = neighbors_list
        heuristic_values[node_name] = h_value
    start_node = input("Enter start node: ").strip()
    final_path = simple_hill_climbing(graph, start_node, heuristic_values)
    print(" -> ".join(final_path))


# s, a b c, 17
# a, e, 10
# b, e d, 13
# c, d, 4
# e, f, 4
# d, f, 2
# f, g, 1
# g, , 0