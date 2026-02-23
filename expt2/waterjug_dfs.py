from math import gcd
def water_jug_dfs(jug1_capacity, jug2_capacity, target):
    visited = set()
    all_paths = []
    def dfs(jug1, jug2, path):
        if jug1 == target or jug2 == target:
            all_paths.append(path + [(jug1, jug2)])
            return
        state = (jug1, jug2)
        if state in visited:
            return
        visited.add(state)
        rules = [
            (jug1_capacity, jug2), 
            (jug1, jug2_capacity),  
            (0, jug2),         
            (jug1, 0),          
            (max(0, jug1 - (jug2_capacity - jug2)), min(jug2_capacity, jug1 + jug2)),
            (min(jug1_capacity, jug1 + jug2), max(0, jug2 - (jug1_capacity - jug1)))
        ]
        for next_state in rules:
            dfs(next_state[0], next_state[1], path + [state])
    dfs(0, 0, [])
    return all_paths if all_paths else None
if __name__ == "__main__":
    jug1_cap, jug2_cap = map(int, input("Enter capacities of Jugs: ").split())
    target = int(input("Enter the target amount: "))
    if target > max(jug1_cap, jug2_cap) or target % gcd(jug1_cap, jug2_cap) != 0:
        print("\nNo solution possible with given capacities.")
    else:
        result = water_jug_dfs(jug1_cap, jug2_cap, target)
        if result:
            print("\n" + "="*50)
            print(f"DFS SOLUTIONS")
            print("="*50)
            for path_num, path in enumerate(result, start=1):
                print(f"\nSolution Path {path_num}")
                print("-"*30)
                for step, state in enumerate(path):
                    print(f"Step {step:2d} -> Jug1: {state[0]:2d} | Jug2: {state[1]:2d}")
                print("-"*30)
            print(f"\nTotal Solutions Found: {len(result)}")