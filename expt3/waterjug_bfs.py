from collections import deque
from math import gcd

def water_jug_bfs(jug1_capacity, jug2_capacity, target):
    start = (0, 0)
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    solutions = []

    while queue:
        jug1, jug2 = queue.popleft()

        if jug1 == target or jug2 == target:
            path = []
            state = (jug1, jug2)
            while state is not None:
                path.append(state)
                state = parent[state]
            solutions.append(list(reversed(path)))
            continue

        rules = [
            (jug1_capacity, jug2),
            (jug1, jug2_capacity),
            (0, jug2),
            (jug1, 0),
            (max(0, jug1 - (jug2_capacity - jug2)),
             min(jug2_capacity, jug1 + jug2)),
            (min(jug1_capacity, jug1 + jug2),
             max(0, jug2 - (jug1_capacity - jug1)))
        ]

        for next_state in rules:
            if next_state not in visited:
                visited.add(next_state)
                parent[next_state] = (jug1, jug2)
                queue.append(next_state)

    return solutions if solutions else None


if __name__ == "__main__":
    jug1_cap, jug2_cap = map(int, input("Enter capacities of Jugs: ").split())
    target = int(input("Enter the target amount: "))

    if target > max(jug1_cap, jug2_cap) or target % gcd(jug1_cap, jug2_cap) != 0:
        print("\nNo solution possible with given capacities.")
    else:
        results = water_jug_bfs(jug1_cap, jug2_cap, target)

        if results:
            print("\n" + "="*50)
            print(f"BFS SOLUTIONS")
            print("="*50)

            for sol_num, result in enumerate(results, start=1):
                print(f"\nSolution Path {sol_num}")
                print("-"*30)

                for step, state in enumerate(result):
                    print(f"Step {step:2d} -> Jug1: {state[0]:2d} | Jug2: {state[1]:2d}")

                print("-"*30)

            print(f"\nTotal Solutions Found: {len(results)}")
