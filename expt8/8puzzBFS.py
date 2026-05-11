import copy 

def heuristic(state, goal_state): 
    misplaced = 0 
    for i in range(3): 
        for j in range(3): 
            if state[i][j] != 0: 
                if state[i][j] != goal_state[i][j]: 
                    misplaced += 1 
    return misplaced 

def moveGen(state): 
    moves = [] 
    x, y = -1, -1 
    
    # Find the blank tile (0)
    for i in range(3): 
        for j in range(3): 
            if state[i][j] == 0: 
                x, y = i, j 
                break 
        if x != -1:
            break
            
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] 
    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy 
        if 0 <= new_x < 3 and 0 <= new_y < 3: 
            new_state = copy.deepcopy(state) 
            # Swap the blank tile with the adjacent tile
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y] 
            moves.append(new_state) 
            
    return moves 

def GoalTest(state, goal_state): 
    return state == goal_state 

def OccursIn(state, listOfPairs): 
    for pair in listOfPairs: 
        if state == pair[0]: 
            return True 
    return False 

def RemoveSeen(childList, openList, closedList): 
    newChildren = [] 
    for child in childList: 
        if not OccursIn(child, openList) and not OccursIn(child, closedList): 
            newChildren.append(child) 
    return newChildren 

def MakePairs(nodes, parent, goal_state): 
    pairs = [] 
    for i in nodes: 
        pairs.append((i, parent, heuristic(i, goal_state))) 
    return pairs 

def PrintState(state): 
    for row in state: 
        print(" ".join(map(str, row))) 

def ReconstructPath(nodePair, closed, goal_state): 
    path = [nodePair[0]] 
    parent = nodePair[1] 
    
    while parent is not None: 
        path.insert(0, parent) 
        found_parent = None 
        for pair in closed: 
            if pair[0] == parent: 
                found_parent = pair 
                break 
        if found_parent: 
            parent = found_parent[1] 
        else: 
            break 
            
    print("\nPath to Goal:") 
    for idx, state in enumerate(path): 
        print(f"\nStep {idx + 1}:") 
        PrintState(state) 
        h_val = heuristic(state, goal_state) 
        print("Heuristic value = " + str(h_val)) 
        
    return path 

def BestFirstSearch(initial_state, goal_state): 
    # List format: (state, parent_state, heuristic_value)
    openList = [(initial_state, None, heuristic(initial_state, goal_state))] 
    closed = [] 
    step = 1 
    
    while openList: 
        openList.sort(key=lambda x: x[2]) 
        nodePair = openList.pop(0) 
        n = nodePair[0] 
        
        print(f"Step {step} - Exploring state with h={nodePair[2]}")
        step += 1 
        
        if GoalTest(n, goal_state): 
            print("\nGoal found!") 
            return ReconstructPath(nodePair, closed, goal_state) 
            
        closed.append(nodePair) 
        children = moveGen(n) 
        noLoops = RemoveSeen(children, openList, closed) 
        newPairs = MakePairs(noLoops, n, goal_state) 
        openList.extend(newPairs)
        
    print("Goal not reachable.") 
    return None 

if __name__ == "__main__":
    print("Enter the start state (3x3, space-separated):") 
    initial_state = [list(map(int, input().split())) for _ in range(3)] 
    
    print("\nEnter the goal state (3x3, space-separated):") 
    goal_state = [list(map(int, input().split())) for _ in range(3)] 
    
    BestFirstSearch(initial_state, goal_state)