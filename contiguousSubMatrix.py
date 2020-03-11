
import pprint
import random

def solve(matrix=None, size=25):
    '''
    args
        matrix: a list of lists of ints
    
    TODO: optimizations
    1. create memo for each value v in single pass, then iterate for solutions
    2. supplant max_offset with list of candidates
        shortcoming now is that if max_offset = 5, but there's only one row with 5-contiguous for value v, 5 is not a possible n for solution
        combine with optimization 1 above to examine the v with the largest n candidate size first, then iterated descending
    '''
    
    if not matrix:
        matrix = [
                    [random.choice([0,1]) for _ in range(size)] for _ in range(size)
        ]
    
    H = len(matrix)
    L = len(matrix[0])
    pprint.pprint(matrix)
    vals = get_unique_values(matrix, H, L)
    print('*'*50)
    print(f'unique values in matrix: {vals}')
    
    global_solution = {'i':0,'j':0,'n':1,'v':matrix[0][0]}
    
    # for each unique value entry in matrix
    for v in vals:
        current_solution = None
        print()
        print('*'*50)
        print(f'current val = {v}')
        memo, max_offset = get_memos(v, matrix, H, L)
        #pprint.pprint(memo)
        print(f'max_offset = {max_offset}')
        
        # for all possible NxNs, descending
        # starting with max_offset from memos
        # ending with NxN size is global solution
        for o in range(max_offset, global_solution['n'], -1):
            i = 0
            
            while i < len(memo):
                row = memo[i]
                inc = 1
                
                # for all origin candidates of i-contiguous runs
                for j in row[o]:
                    offset = 1
                    
                    while i+offset < len(memo) and j in memo[i+offset][o]:  
                        offset += 1
                        inc += offset
                        if offset == o:
                            current_solution = {'i':i,'j':j,'n':offset,'v':v}
                            print(f"Local Solution Found: {current_solution}")
                            break
                    if current_solution:
                        break
                if current_solution:
                    break
                i += inc
            if current_solution:
                    break
        
        if current_solution and current_solution['n'] > global_solution['n']:
            global_solution = current_solution
    
    print()
    print('*'*50)
    print(f"Global Solution: {global_solution}")
    print('*'*50)
                                    
        
    
def get_unique_values(matrix, H, L):
    s = set()
    for i in range(H):
        for j in range(L):
            s.add(matrix[i][j])
    return s

def get_memos(v, matrix, H, L):
    '''local_candidates = [0 for x in range(L+1)]'''
    max_offset = 1
    m = [
            [
                [] for i in range(L+1)
            ] for i in range(H)
        ]
    
    for i in range(H):
        j = 0
        '''valid_row = False'''
        while j < L-1: # because we only care about N-contiguous where N>1, don't choose origin at last val in row
            if matrix[i][j] != v:
                # move origin to the right
                j += 1
                continue
            
            offset = 1
            while (j + offset < L) and (matrix[i][j+offset] == v):
                offset += 1
            
            if offset > 1:
                max_offset = max(offset, max_offset)
                '''
                if not valid_row:
                    valid_row = True
                    local_candidates[offset] += 1
                print(f'local_candidates {local_candidates}')
                '''
                for k in range(offset-1):
                    #m[i][offset-k].append(j+k) # this is a feasible lookup but less intuitive during later traversal
                    m[i][offset-k] += [x for x in range(j, j+k+1)]
                    
            j += offset
    '''
    candidates = []
    for i in range(2, len(local_candidates)):
        if local_candidates[i] >= i:
            candidates.append(i)
    print(f'candidates {candidates}')
    return m, candidates
    '''
    return m, max_offset


if __name__ == '__main__':
	solve()