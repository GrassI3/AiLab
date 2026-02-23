def IsValid(M, C, TotalM, TotalC):
    if M < 0 or C < 0 or M > TotalM or C > TotalC:
        return False
    if M > 0 and M < C:
        return False
    if (TotalM - M) > 0 and (TotalM - M) < (TotalC - C):
        return False
    return True

def misCan_dfs(StartM, StartC):
    Visited = set()
    AllPaths = []
    def Dfs(M, C, B, Path):
        State = (M, C, B)
        if M == 0 and C == 0:
            AllPaths.append(Path + [State])
            return
        if State in Visited:
            return
        Visited.add(State)
        Rules = [(1, 0), (2, 0), (1, 1), (0, 1), (0, 2)]
        for Dm, Dc in Rules:
            if B == 0:
                NewM, NewC, NewB = M - Dm, C - Dc, 1
            else:
                NewM, NewC, NewB = M + Dm, C + Dc, 0
            if IsValid(NewM, NewC, StartM, StartC):
                Dfs(NewM, NewC, NewB, Path + [State])
    Dfs(StartM, StartC, 0, [])
    return AllPaths
if __name__ == "__main__":
    MCount, CCount = map(int, input("Enter total Missionaries and Cannibals: ").split())  
    if CCount > MCount and MCount > 0:
        print("\nInvalid initial state.")
    else:
        Result = misCan_dfs(MCount, CCount)
        if Result:
            print(f"\n{'='*20} MISSONARIES AND CANNIBALS DFS {'='*20}")
            for I, Path in enumerate(Result, 1):
                print(f"\nPath {I}:")
                for Step, (M, C, B) in enumerate(Path):
                    Side = "Left" if B == 0 else "Right"
                    #print(f"  Step {Step}: L({M}M, {C}C) | Boat: {Side} | R({MCount-M}M, {CCount-C}C)")
                    print(f"  Step {Step}: ({M}M, {C}C," f" {'L' if B == 0 else 'R'})")
            print(f"\nTotal: {len(Result)}")
        else:
            print("\nNo solution.")