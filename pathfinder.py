import sys
from collections import deque
import math
import heapq
STUDENT_ID = 'a1891628' # your student ID
DEGREE = 'UG'

def parse_map(map_name):
    try:
        with open(map_name, 'r') as file:
            lines = file.readlines()

            rows, cols = map(int, lines[0].strip().split())

            start = tuple(map(int, lines[1].strip().split()))
            end = tuple(map(int, lines[2].strip().split()))

            grid = []
            for line in lines[3:]:
                row = []
                for token in line.strip().split():
                    if token == 'X':
                         row.append(token)
                    else:
                        row.append(int(token))
                grid.append(row)

            return rows, cols, start, end, grid
    except Exception as e:
        print(f"Error in reading map file")
        sys.exit(1)

def format_grid(matrix):
    return [[str(x) if x is not None else '.' for x in row]for row in matrix]

def bfs(rows, cols, start, end, grid, mode):

    start = (start[0] - 1, start[1] - 1)
    end = (end[0] - 1, end[0] -1)

    visits = [[0 for j in range(cols)] for i in range(rows)]
    firstVisit = [[None for j in range(cols)] for i in range(rows)]
    lastVisit = [[None for j in range(cols)] for i in range(rows)]

    startNode = (start[0], start[1], None)

    queue = deque()
    queue.append(startNode)
    closed = set()

    counter = 0
    goalNode = None

    while queue:
        node = queue.popleft()
        r, c, parent = node
        counter += 1
        
        visits[r][c] += 1
        if firstVisit[r][c] is None:
            firstVisit[r][c] = counter
        lastVisit[r][c] = counter

        if (r, c) == end:
            goalNode = node
            break

        if (r, c) not in closed:
            closed.add((r, c))
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 'X':
                    neighbourNode = (nr, nc, node)
                    queue.append(neighbourNode)
        
    if goalNode is None:
        print("null")
        return
    
    path = []
    node = goalNode
    while node is not None:
        r, c, parent = node
        path.append((r, c))
        node = parent
    path.reverse()

    pathGrid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if (i, j) in path:
                row.append('*')
            else:
                row.append('X' if grid[i][j] == 'X' else str(grid[i][j]))
        pathGrid.append(row)

    visitsDisplay = format_grid(visits)
    firstVisitDisplay = format_grid(firstVisit)
    lastVisitDisplay = format_grid(lastVisit)

    if mode == 'release':
        for row in pathGrid:
            print(" ".join(row))
    elif mode == 'debug':
        print("path:")
        for row in pathGrid:
            print(" ".join(row))
        
        print("\n#visits:")
        for row in visitsDisplay:
            print(" ".join(row))
        
        print("\nfirst visit:")
        for row in firstVisitDisplay:
            print(" ".join(row))
        
        print("\nlast visit:")
        for row in lastVisitDisplay:
            print(" ".join(row))


def ucs(rows, cols, start, end, grid, mode):
    start = (start[0] - 1, start[1] - 1)
    end   = (end[0] - 1, end[1] - 1)

    costGrid = [[math.inf for col in range(cols)] for row in range(rows)]
    costGrid[start[0]][start[1]] = 0

    visits = [[0 for col in range(cols)] for row in range(rows)]
    firstVisit = [[None for col in range(cols)] for row in range(rows)]
    lastVisit = [[None for col in range(cols)] for row in range(rows)]

    parent = [[None for col in range(cols)] for row in range(rows)]

    currentNodes = []
    insertionCounter = 0
    heapq.heappush(currentNodes, (0, insertionCounter, start[0], start[1]))
    insertionCounter += 1

    counter = 0
    goalFound = False

    while currentNodes:
        currentCost, order, r, c = heapq.heappop(currentNodes)
        counter += 1

        if currentCost > costGrid[r][c]:continue

        visits[r][c] += 1
        if firstVisit[r][c] is None:
            firstVisit[r][c] = counter
        lastVisit[r][c] = counter

        if (r, c) == end:
            goalFound = True
            break

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 'X':
                currentElevation = grid[r][c]
                nextElevation = grid[nr][nc]
                if nextElevation > currentElevation:
                    stepCost = 1 + (nextElevation - currentElevation)
                else:
                    stepCost = 1
                newCost = currentCost + stepCost

                if newCost < costGrid[nr][nc]:
                    costGrid[nr][nc] = newCost
                    parent[nr][nc] = (r, c)
                    heapq.heappush(currentNodes, (newCost, insertionCounter, nr, nc))
                    insertionCounter += 1

    if goalFound == False:
        print("nulddl")
        return

    path = []
    pr, pc = end
    while (pr, pc) is not None:
        path.append((pr, pc))
        if parent[pr][pc] is None:
            break
        pr, pc = parent[pr][pc]
    path.reverse()

    totalCost = costGrid[end[0]][end[1]]

    pathGrid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if (i, j) in path:
                row.append('*')
            else:
                row.append(str(grid[i][j]) if grid[i][j] != 'X' else 'X')
        pathGrid.append(row)

    visitsDisplay = format_grid(visits)
    firstVisitDisplay = format_grid(firstVisit)
    lastVisitDisplay = format_grid(lastVisit)

    # print(f"Total cost: {totalCost}\n")
    
    if mode == 'release':
        for row in pathGrid:
            print(" ".join(row))
    elif mode == 'debug':
        print("path:")
        for row in pathGrid:
            print(" ".join(row))
        print("\n#visits:")
        for row in visitsDisplay:
            print(" ".join(row))
        print("\nfirst visit:")
        for row in firstVisitDisplay:
            print(" ".join(row))
        print("\nlast visit:")
        for row in lastVisitDisplay:
            print(" ".join(row))

def astar(rows, cols, start, end, grid, mode, heuristic):
    start = (start[0] - 1, start[1] - 1)
    end   = (end[0] - 1, end[1] - 1)

    costGrid = [[math.inf for col in range(cols)] for row in range(rows)]
    costGrid[start[0]][start[1]] = 0

    visits = [[0 for col in range(cols)] for row in range(rows)]
    firstVisit = [[None for col in range(cols)] for row in range(rows)]
    lastVisit = [[None for col in range(cols)] for row in range(rows)]

    parent = [[None for col in range(cols)] for row in range(rows)]

    currentNodes = []
    insertionCounter = 0

    def manhattan(row, col):
        return abs(row - end[0]) + abs(col - end[1])
    
    def euclidean(row, col):
        return math.sqrt((row - end[0])**2 + (col - end[1])**2)
    
    if heuristic == "manhattan":
        heuristicDistanceStart = manhattan(start[0], start[1])
    elif heuristic == "euclidean":
        heuristicDistanceStart = euclidean(start[0], start[1])

    estimateValueStart = 0 + heuristicDistanceStart

    # a tuple of estiamted cost, insertion counter, cumulative cost, row, col, 
    heapq.heappush(currentNodes, (estimateValueStart, insertionCounter, 0, start[0], start[1]))
    insertionCounter += 1

    counter = 0
    goalFound = False

    while currentNodes:
        currentEstimate, notused, currentCost, r, c = heapq.heappop(currentNodes)
        counter += 1

        if currentCost > costGrid[r][c]:
            continue

        visits[r][c] += 1
        if firstVisit[r][c] is None:
            firstVisit[r][c] = counter
        lastVisit[r][c] = counter

        if (r, c) == end:
            goalFound = True
            break
        
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 'X':
                currentElevation = grid[r][c]
                nextElevation = grid[nr][nc]
                if nextElevation > currentElevation:
                    stepCost = 1 + (nextElevation - currentElevation)
                else:
                    stepCost = 1
                newCost = currentCost + stepCost

                if newCost < costGrid[nr][nc]:
                    costGrid[nr][nc] = newCost
                    parent[nr][nc] = (r, c)

                    if heuristic == "manhattan":
                        newHeuristic = manhattan(nr, nc)
                    elif heuristic == "euclidean":
                        newHeuristic = euclidean(nr, nc)

                    newEstimate = newCost + newHeuristic
                    heapq.heappush(currentNodes, (newEstimate, insertionCounter, newCost, nr, nc))
                    insertionCounter += 1

    if goalFound == False:
            print("null")
            return

    path = []
    pr, pc = end
    while (pr, pc) is not None:
        path.append((pr, pc))
        if parent[pr][pc] is None:
            break
        pr, pc = parent[pr][pc]
    path.reverse()


    pathGrid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if (i, j) in path:
                row.append('*')
            else:
                row.append(str(grid[i][j]) if grid[i][j] != 'X' else 'X')
        pathGrid.append(row)

    visitsDisplay = format_grid(visits)
    firstVisitDisplay = format_grid(firstVisit)
    lastVisitDisplay = format_grid(lastVisit)
    
    if mode == 'release':
        for row in pathGrid:
            print(" ".join(row))
    elif mode == 'debug':
        print("path:")
        for row in pathGrid:
            print(" ".join(row))
        print("\n#visits:")
        for row in visitsDisplay:
            print(" ".join(row))
        print("\nfirst visit:")
        for row in firstVisitDisplay:
            print(" ".join(row))
        print("\nlast visit:")
        for row in lastVisitDisplay:
            print(" ".join(row))


if __name__ == "__main__":
    if len(sys.argv) < 4 or (sys.argv[3] == "astar" and len(sys.argv) < 5):
        print("Usage: python pathfinder.py [mode] [map] [algorithm] [heuristic]")
        sys.exit(1)

    mode = sys.argv[1]
    map_name = sys.argv[2]
    algorithm = sys.argv[3]
    if (algorithm == "astar"):
        heuristic = sys.argv[4]
    else:
        None

    rows, cols, start, end, grid = parse_map(map_name)

    if algorithm == 'bfs':
        # call bfs function
        bfs(rows, cols, start, end, grid, mode)
        pass
    elif algorithm == 'ucs':
        # call ucs function
        ucs(rows, cols, start, end, grid, mode)
        pass
    elif algorithm == 'astar':
        #call astar function
        astar(rows, cols, start, end, grid, mode, heuristic)
        pass


"""
    print(mode)
    print(algorithm)
    print(rows)
    print(cols)
    print(start)
    print(end)
    print(grid)
"""

"""start the pathfinding program:
    
    how its gonna work:
     just each function is a different type of search, and they will be called 
     depending on which type of function is needed.
     
    Each function would store every matrix of information needed for debug, but whether 
    they are outputted or not it is up to the input."""
