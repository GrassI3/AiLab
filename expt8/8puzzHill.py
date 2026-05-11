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
            new_state = [row[:] for row in state] 
            new_state[x][y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[x][y] 
            moves.append(new_state) 
            
    return moves 

def hill_climbing(initial_state, goal_state): 
    visited = [] 
    state = initial_state 
    visited.append(state) 
    
    while True:
        neighbors = moveGen(state) 
        neighbors.sort(key=lambda x: heuristic(x, goal_state)) 
        
        if not neighbors: 
            print("No neighbors available.") 
            break 
            
        new_state = neighbors[0] 
        
        if heuristic(new_state, goal_state) < heuristic(state, goal_state): 
            state = new_state 
            visited.append(state) 
        else: 
            break 

    if state == goal_state: 
        print("\nGoal state reached!") 
    else: 
        print("\nLocal Optimum reached, goal state not found.") 
        
    print("Sequence of Visited States:") 
    i = 1 
    for s in visited: 
        print("\nStep " + str(i) + ":") 
        for row in s: 
            for val in row: 
                print(val, end=" ") 
            print() 
        h_val = heuristic(s, goal_state) 
        print("Heuristic value = " + str(h_val)) 
        i += 1 

if __name__ == "__main__":
    print("Enter the start state (3 rows, space-separated):") 
    initial_state = [] 
    for i in range(3): 
        row = list(map(int, input().split())) 
        initial_state.append(row) 
        
    print("\nEnter the goal state (3 rows, space-separated):") 
    goal_state = [] 
    for i in range(3): 
        row = list(map(int, input().split())) 
        goal_state.append(row) 
        
    hill_climbing(initial_state, goal_state)