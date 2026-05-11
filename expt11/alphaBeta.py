import math 
import sys

def alphabeta(node, alpha, beta, tree, evals, depth=0): 
    indent = "  " * depth 
    children = tree.get(node, []) 
    
    if not children: 
        if node not in evals:
            print(f"{indent}Terminal {node} has no value! Defaulting to 0.")
            return 0
            
        print(f"{indent}Terminal {node} = {evals[node]}") 
        return evals[node]
        
    is_max = depth % 2 == 0 
    
    if is_max: 
        print(f"{indent}MAX node {node} (a={_f(alpha)}, b={_f(beta)})") 
        for child in children: 
            alpha = max(alpha, alphabeta(child, alpha, beta, tree, evals, depth+1)) 
            print(f"{indent}  a updated to {_f(alpha)}") 
            if alpha >= beta: 
                print(f"{indent}  >> b-pruning") 
                return beta 
        return alpha 
    else: 
        print(f"{indent}MIN node {node} (a={_f(alpha)}, b={_f(beta)})") 
        for child in children: 
            beta = min(beta, alphabeta(child, alpha, beta, tree, evals, depth+1)) 
            print(f"{indent}  b updated to {_f(beta)}") 
            if alpha >= beta: 
                print(f"{indent}  >> a-pruning") 
                return alpha 
        return beta 

def _f(v): 
    if v == math.inf: return "+inf" 
    if v == -math.inf: return "-inf" 
    return str(v) 

if __name__ == "__main__":
    print("Alpha-Beta Pruning") 
    print("==================") 
    print("PASTE your entire tree below. Type 'done' on a new line when finished.")
    print("Format -> Parent: Node Child1, Child2 (e.g., L LL, LR)")
    print("Format -> Leaf:   Node Value (e.g., a 10)\n")
    
    tree = {} 
    evals = {} 
    root = None 
    
    while True: 
        try:
            line = input().strip() 
        except EOFError:
            break 
            
        if not line:
            continue
            
        if line.lower() == "done": 
            break 
            
        line = line.replace("Node (or done):", "").replace("Value of leaf", "").strip()
        
        parts = line.split(maxsplit=1) 
        if len(parts) < 2:
            continue
            
        node = parts[0].replace(':', '') 
        rest = parts[1] 
        
        if root is None: 
            root = node 
            
        try:
            val = int(rest.strip()) 
            evals[node] = val 
            tree[node] = [] 
        except ValueError:
            children = [c.strip() for c in rest.replace(',', ' ').split() if c.strip()]
            tree[node] = children 

    print("\n--- Starting Alpha-Beta Search ---\n") 
    
    if root is not None:
        result = alphabeta(root, -math.inf, math.inf, tree, evals) 
        print(f"\nFinal Result: {result}")
    else:
        print("No tree data was entered.")