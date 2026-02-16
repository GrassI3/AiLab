from collections import deque

def bfs(start, graph):
    visited = set()
    queue = deque([start])
    result = []
    
    while queue:
        node = queue.popleft()
        if node not in visited:
            visited.add(node)
            result.append(node)
            if node in graph:
                queue.extend(graph[node])
    return result

if __name__ == "__main__":
    graph = {}
    num_nodes = int(input("Enter the number of nodes: "))
    
    for i in range(num_nodes):
        node = input("Enter node name: ")
        neighbours = input(f"Enter neighbors of {node}: ").split()
        graph[node] = neighbours
    
    start_node = input("Enter the starting node: ")
    print(bfs(start_node, graph))