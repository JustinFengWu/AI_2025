import sys
from collections import deque
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
            for dr, dc in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 'X':
                    neighbourNode = (nr, nc, node)
                    queue.append(neighbourNode)
        
    if goalNode is None:
        print("goal unreached")
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

    def format_grid(matrix):
        return [[str(x) if x is not None else '.' for x in row]for row in matrix]

    visitsDisplay = format_grid(visits)
    firstVisitDisplay = format_grid(firstVisit)
    lastVisitDisplay = format_grid(lastVisit)

    if mode == 'release':
        print("path:")
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
        pass
    elif algorithm == 'astar':
        #call astar function
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
