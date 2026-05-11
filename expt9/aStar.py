class Node:
    def __init__(self, name, parent, g, h):
        self.name = name
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h
    def __str__(self):
        parent_name = self.parent if self.parent is not None else "Nil"
        return f"({self.name},{parent_name},{self.g},{self.h},{self.f})"
def a_star(graph, heuristics, start, goal):
    open_list = [Node(start, None, 0, heuristics[start])]
    closed_list = []
    history = []
    while open_list:
        open_list.sort(key=lambda n: (n.f, n.name))
        open_str = ", ".join(str(node) for node in open_list)
        closed_str = ", ".join(str(node) for node in closed_list)
        history.append(f"{open_str:<45} | {closed_str}")
        current = open_list.pop(0)
        closed_list.append(current)
        if current.name == goal:
            print(f"\n{'open':<45} | closed")
            print("-" * 80)
            for state in history:
                print(state)
            print("-" * 80)
            print("Goal Reached!")
            path = []
            curr = current
            while curr:
                path.append(curr.name)
                curr = next((node for node in closed_list if node.name == curr.parent), None)
            print(f"Final Path: {' -> '.join(path[::-1])}")
            return
        if current.name in graph:
            for neighbor, cost in graph[current.name].items():
                g = current.g + cost
                h = heuristics[neighbor]
                in_closed = False
                for c_node in closed_list:
                    if c_node.name == neighbor:
                        in_closed = True
                        if g < c_node.g:
                            c_node.g = g
                            c_node.f = g + h
                            c_node.parent = current.name
                            stack = [c_node]
                            while stack:
                                p_node = stack.pop(0)
                                if p_node.name in graph:
                                    for n_name, n_cost in graph[p_node.name].items():
                                        new_g = p_node.g + n_cost
                                        for desc in open_list + closed_list:
                                            if desc.name == n_name and new_g < desc.g:
                                                desc.g = new_g
                                                desc.f = new_g + heuristics[n_name]
                                                desc.parent = p_node.name
                                                stack.append(desc)
                        break
                if in_closed:
                    continue
                in_open = False
                for o_node in open_list:
                    if o_node.name == neighbor:
                        in_open = True
                        if g < o_node.g:
                            o_node.g = g
                            o_node.f = g + h
                            o_node.parent = current.name
                        break
                if not in_open:
                    open_list.append(Node(neighbor, current.name, g, h))
    print(f"\n{'open':<45} | closed")
    print("-" * 80)
    for state in history:
        print(state)
    print("\nGoal not reachable.")
if __name__ == "__main__":
    graph, heuristic_values = {}, {}
    print("Enter node, neighbours, heuristic value:")
    while True:
        line = input().strip()
        if not line: break
        parts = [p.strip() for p in line.split(',')]
        node_name = parts[0]
        graph[node_name] = {}
        if len(parts) > 1 and parts[1]:
            neighbors_data = parts[1].split()
            for i in range(0, len(neighbors_data), 2):
                n = neighbors_data[i]
                cost = int(neighbors_data[i+1])
                graph[node_name][n] = cost
        if len(parts) > 2:
            heuristic_values[node_name] = int(parts[2])
    start_node = input("Enter start node: ").strip()
    goal_node = input("Enter goal node: ").strip()
    a_star(graph, heuristic_values, start_node, goal_node)

# s, a 6 b 5 c 10, 17
# a, e 6, 10
# b, e 6 d 7, 13
# c, d 6, 4
# e, f 4, 4
# d, f 6, 2
# f, g 3, 1
# g, , 0