from collections import deque
def IsValid(M, C, TotalM, TotalC):
    if M < 0 or C < 0 or M > TotalM or C > TotalC:
        return False
    if M > 0 and M < C:
        return False
    if (TotalM - M) > 0 and (TotalM - M) < (TotalC - C):
        return False
    return True
def misCan_bfs(StartM, StartC):
    start_state = (StartM, StartC, 0)
    queue = deque([(start_state, [])])
    AllPaths = []
    while queue:
        (M, C, B), path = queue.popleft()
        if M == 0 and C == 0:
            AllPaths.append(path + [(M, C, B)])
            continue 
        Rules = [(1, 0), (2, 0), (1, 1), (0, 1), (0, 2)]
        for Dm, Dc in Rules:
            if B == 0:
                NewM, NewC, NewB = M - Dm, C - Dc, 1
            else:
                NewM, NewC, NewB = M + Dm, C + Dc, 0
            new_state = (NewM, NewC, NewB)
            if IsValid(NewM, NewC, StartM, StartC):
                if new_state not in path:
                    queue.append((new_state, path + [(M, C, B)]))
    return AllPaths
if __name__ == "__main__":
    input_data = input("Enter total Missionaries and Cannibals: ").split()
    if len(input_data) >= 2:
        MCount, CCount = map(int, input_data)  
        if CCount > MCount and MCount > 0:
            print("\nInvalid initial state.")
        else:
            Result = misCan_bfs(MCount, CCount)
            if Result:
                print(f"\n{'='*20} MISSIONARIES AND CANNIBALS BFS {'='*20}")
                for I, Path in enumerate(Result, 1):
                    print(f"\nPath {I}:")
                    for Step, (M, C, B) in enumerate(Path):
                        side_char = 'L' if B == 0 else 'R'
                        print(f"  Step {Step}: ({M}M, {C}C, {side_char})")
                print(f"\nTotal: {len(Result)}")
            else:
                print("\nNo solution.")