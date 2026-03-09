import heapq
def bestfs(start, goal, graph, heuristic):
    visited = []
    queue = [(heuristic[start], start)]
    parent = {start: None} 
    print(f"\n{'OPEN':<{75}} | {'CLOSED'}")
    print("-" * (125))
    def find_link(n): return parent.get(n).upper() if parent.get(n) else "Nil"
    while queue:
        _, node = heapq.heappop(queue)
        if node not in visited:
            visited.append(node)
            if node != goal and node in graph:
                for neighbor in graph[node]:
                    if neighbor not in visited:
                        if neighbor not in parent:
                            parent[neighbor] = node
                        heapq.heappush(queue, (heuristic[neighbor], neighbor))
            if node == goal:
                print("Goal Found!")
                break
            OPEN = ", ".join([f"({n.upper()}, {find_link(n)}, {h})" for h, n in sorted(queue)])
            CLOSED = ", ".join([f"({n.upper()}, {find_link(n)}, {heuristic[n]})" for n in visited])
            print(f"{OPEN:<{75}} | {CLOSED}")
    path = []
    current = goal
    if current in visited:
        while current is not None:
            path.append(current)
            current = parent.get(current)
        path.reverse()
        return " -> ".join([p.upper() for p in path])
    else:
        return "Goal not reachable"
if __name__ == "__main__":
    graph = {}
    heuristics = {}
    print("Enter Node, Heuristic and Neighbours. Press Enter twice when done:")
    while True:
        line = input()
        if not line.strip():
            break
        parts = line.split()
        node = parts[0]
        heuristics[node] = int(parts[1])
        graph[node] = parts[2:]
    start_node = input("Enter the starting node: ")
    goal_node = input("Enter the goal node: ")
    final_path = bestfs(start_node, goal_node, graph, heuristics)
    print(f"\nPath: {final_path}")


# a 20 b c d
# b 15 e f g
# c 14 h i
# d 12 j k
# e 6
# f 5
# g 0
# h 4
# i 5
# j 7
# k 8