def simple_hill_climbing(graph, start, heuristic_values):
    current = start
    path = [current]
    while True:
        neighbors = graph.get(current, [])
        next_node = None
        for neighbor in neighbors:
            if neighbor in heuristic_values and heuristic_values[neighbor] < heuristic_values[current]:
                if next_node is None or heuristic_values[neighbor] < heuristic_values[next_node]:
                    next_node = neighbor    
        if next_node is None:
            break
        current = next_node
        path.append(current)
    return path

if __name__ == "__main__":
    graph, heuristic_values = {}, {}
    print("Enter node, neighbours, heuristic value:")
    while True:
        line = input().strip()
        if not line: break
        parts = [p.strip() for p in line.split(',')]
        node_name = parts[0]
        graph[node_name] = parts[1].split()
        heuristic_values[node_name] = int(parts[2])
    start_node = input("Enter start node: ").strip()
    final_path = simple_hill_climbing(graph, start_node, heuristic_values)
    print(" -> ".join(final_path))