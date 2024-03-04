import copy

class Entity:
    def __init__(self, name, grid):
        self.name = name
        self.grid = grid
        self.cellsOn = []
        #self.getCellsOn()
        
    def getCellsOn(self):
        self.cellsOn = []
        rows = len(self.grid)
        cols = len(self.grid[0])
        for row in range(0, rows):
            for col in range(0, cols):
                cell = (row, col)
                if self.grid[row][col] == 1:
                    self.cellsOn.append(cell)

def simulation(currentGrid, nextGrid, width, height, entities, entitiesCount):
    checkedCells = []
    cellsOn = []
    for row in range(1, height+1):
        for column in range(1, width+1):
            cell = (row, column)
            if cell not in checkedCells:
                checkedCells += checkEntities(currentGrid, row, column, entities, entitiesCount)
            neighbours = getOnNeighbours(cell, currentGrid)
            state = currentGrid[row][column]
            applyRules(nextGrid, row, column, state, neighbours)
            if state == ON:
                cellsOn.append(cell)
    #otherEntities = checkOtherEntities(currentGrid, checkedCells, cellsOn)
    #entitiesCount["other"] = otherEntities

def rotateGrid(grid):
    transposedGrid = [list(row) for row in zip(*grid)]
    rotatedGrid = [list(reversed(row)) for row in transposedGrid]
    return rotatedGrid

def mirrorGrid(matrix):
    return [list(reversed(row)) for row in matrix]

def createBlockEntity():
    name = "block"
    grids = {}
    grid = [
            [0,   0,   0, 0], 
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0,   0,   0, 0]
            ]
    grids[1] = grid
    return Entity(name, grids)

def createBeehiveEntity():
    name = "beehive"
    grids = {}
    grid = [
            [0,   0,   0,   0,   0, 0], 
            [0,   0, 1, 1,   0, 0],
            [0, 1,   0,   0, 1, 0],
            [0,   0, 1, 1,   0, 0],
            [0,   0,   0,   0,   0, 0]
            ]
    for i in range(1, 3):
        if i == 1:
            grids[i] = rotateGrid(copy.deepcopy(grid))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    return Entity(name, grids)

def createLoafEntity():
    name = "loaf"
    grids = {}
    grid = [
            [0,   0,   0,   0,   0, 0], 
            [0,   0, 1, 1,   0, 0],
            [0, 1,   0,   0, 1, 0],
            [0,   0, 1,   0, 1, 0],
            [0,   0,   0, 1,   0, 0],
            [0,   0,   0,   0,   0, 0]
            ]
    for i in range(1, 5):
        if i == 1:
            grids[i] = rotateGrid(copy.deepcopy(grid))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid = mirrorGrid(copy.deepcopy(grid))
    for i in range(5, 9):
        if i == 5:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    return Entity(name, grids)
 
def createBoatEntity():
    name = "boat"
    grids = {}
    grid = [
            [0,   0,   0,   0, 0], 
            [0, 1, 1,   0, 0],
            [0, 1,   0, 1, 0],
            [0,   0, 1,   0, 0],
            [0,   0,   0,   0, 0]
            ]
    for i in range(1, 5):
        if i == 1:
            grids[i] = rotateGrid(copy.deepcopy(grid))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid = mirrorGrid(copy.deepcopy(grid))
    for i in range(5, 9):
        if i == 5:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    return Entity(name, grids)

def createTubEntity():
    name = "tub"
    grids = {}
    grid = [
            [0,   0,   0,   0, 0], 
            [0,   0, 1,   0, 0],
            [0, 1,   0, 1, 0],
            [0,   0, 1,   0, 0],
            [0,   0,   0,   0, 0]
            ]
    grids[1] = grid
    return Entity(name, grids)

def createBlinkerEntity():
    name = "blinker"
    grids = {}
    grid1 = [
            [0,   0, 0], 
            [0, 1, 0],
            [0, 1, 0],
            [0, 1, 0],
            [0,   0, 0]
            ]
    grid2 = [
            [0,   0,   0,   0, 0],
            [0, 1, 1, 1, 0],
            [0,   0,   0,   0, 0],
            ]
    grids[1] = grid1
    grids[2] = grid2
    return Entity(name, grids)

def createToadEntity():
    name = "toad"
    grids = {}
    grid1 = [
            [0,   0,   0,   0,   0, 0], 
            [0,   0,   0, 1,   0, 0],
            [0, 1,   0,   0, 1, 0],
            [0, 1,   0,   0, 1, 0],
            [0,   0, 1,   0,   0, 0],
            [0,   0,   0,   0,   0, 0]
            ]
    grid2 = [
            [0,   0,   0,   0,   0, 0], 
            [0,   0,   0,   0,   0, 0],
            [0,   0, 1, 1, 1, 0],
            [0, 1, 1, 1,   0, 0],
            [0,   0,   0,   0,   0, 0],
            [0,   0,   0,   0,   0, 0]
            ]
    for i in range(1, 3):
        if i == 1:
            grids[i] = rotateGrid(copy.deepcopy(grid1))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    for i in range(3, 5):
        if i == 3:
            grids[i] = rotateGrid(copy.deepcopy(grid2))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid1 = mirrorGrid(copy.deepcopy(grid1))
    for i in range(5, 7):
        if i == 5:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid1))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid2 = mirrorGrid(copy.deepcopy(grid2))
    for i in range(7, 9):
        if i == 7:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid2))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    return Entity(name, grids)

def createBeaconEntity():
    name = "beacon"
    grids = {}
    grid1 = [
            [0,   0,   0,   0,   0, 0], 
            [0, 1, 1,   0,   0, 0],
            [0, 1, 1,   0,   0, 0],
            [0,   0,   0, 1, 1, 0],
            [0,   0,   0, 1, 1, 0],
            [0,   0,   0,   0,   0, 0]
            ]
    grid2 = [
            [0,   0,   0,   0,   0, 0], 
            [0, 1, 1,   0,   0, 0],
            [0, 1,   0,   0,   0, 0],
            [0,   0,   0,   0, 1, 0],
            [0,   0,   0, 1, 1, 0],
            [0,   0,   0,   0,   0, 0]
            ]
    for i in range(1, 3):
        if i == 1:
            grids[i] = rotateGrid(copy.deepcopy(grid1))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    for i in range(3, 5):
        if i == 3:
            grids[i] = rotateGrid(copy.deepcopy(grid2))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    return Entity(name, grids)

def createGliderEntity():
    name = "glider"
    grids = {}
    grid1 = [
            [0,   0,   0,   0, 0], 
            [0,   0, 1,   0, 0],
            [0,   0,   0, 1, 0],
            [0, 1, 1, 1, 0],
            [0,   0,   0,   0, 0]
            ]
    grid2 = [
            [0,   0,   0,   0, 0], 
            [0, 1,   0, 1, 0],
            [0,   0, 1, 1, 0],
            [0,   0, 1,   0, 0],
            [0,   0,   0,   0, 0]
            ]
    grid3 = [
            [0,   0,   0,   0, 0], 
            [0,   0,   0, 1, 0],
            [0, 1,   0, 1, 0],
            [0,   0, 1, 1, 0],
            [0,   0,   0,   0, 0]
            ]
    grid4 = [
            [0,   0,   0,   0, 0], 
            [0, 1,   0,   0, 0],
            [0,   0, 1, 1, 0],
            [0, 1, 1,   0, 0],
            [0,   0,   0,   0, 0]
            ]
    for i in range(1, 5):
        if i == 1:
            grids[i] = rotateGrid(copy.deepcopy(grid1))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    for i in range(5, 9):
        if i == 5:
            grids[i] = rotateGrid(copy.deepcopy(grid2))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    for i in range(9, 13):
        if i == 9:
            grids[i] = rotateGrid(copy.deepcopy(grid3))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    for i in range(13, 17):
        if i == 13:
            grids[i] = rotateGrid(copy.deepcopy(grid4))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid1 = mirrorGrid(copy.deepcopy(grid1))
    for i in range(17, 21):
        if i == 17:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid1))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid2 = mirrorGrid(copy.deepcopy(grid2))
    for i in range(21, 25):
        if i == 21:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid2))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid3 = mirrorGrid(copy.deepcopy(grid3))
    for i in range(25, 29):
        if i == 25:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid3))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid4 = mirrorGrid(copy.deepcopy(grid4))
    for i in range(29, 33):
        if i == 29:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid4))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    return Entity(name, grids)

def createLightWeightSpaceshipEntity():
    name = "lightWeightSpaceship"
    grids = {}
    grid1 = [
            [0,   0,   0,   0,   0,   0, 0], 
            [0, 1,   0,   0, 1,   0, 0],
            [0,   0,   0,   0,   0, 1, 0],
            [0, 1,   0,   0,   0, 1, 0],
            [0,   0, 1, 1, 1, 1, 0],
            [0,   0,   0,   0,   0,   0, 0]
            ]
    grid2 = [
            [0,   0,   0,   0,   0,   0, 0], 
            [0,   0,   0, 1, 1,   0, 0],
            [0, 1, 1,   0, 1, 1, 0],
            [0, 1, 1, 1, 1,   0, 0],
            [0,   0, 1, 1,   0,   0, 0],
            [0,   0,   0,   0,   0,   0, 0]
            ]
    grid3 = [
            [0,   0,   0,   0,   0,   0, 0], 
            [0,   0, 1, 1, 1, 1, 0],
            [0, 1,   0,   0,   0, 1, 0],
            [0,   0,   0,   0,   0, 1, 0],
            [0, 1,   0,   0, 1,   0, 0],
            [0,   0,   0,   0,   0,   0, 0]
            ]
    grid4 = [
            [0,   0,   0,   0,   0,   0, 0], 
            [0,   0, 1, 1,   0,   0, 0],
            [0, 1, 1, 1, 1,   0, 0],
            [0, 1, 1,   0, 1, 1, 0],
            [0,   0,   0, 1, 1,   0, 0],
            [0,   0,   0,   0,   0,   0, 0]
            ]
    for i in range(1, 5):
        if i == 1:
            grids[i] = rotateGrid(copy.deepcopy(grid1))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    for i in range(5, 9):
        if i == 5:
            grids[i] = rotateGrid(copy.deepcopy(grid2))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    for i in range(9, 13):
        if i == 9:
            grids[i] = rotateGrid(copy.deepcopy(grid3))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    for i in range(13, 17):
        if i == 13:
            grids[i] = rotateGrid(copy.deepcopy(grid4))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid1 = mirrorGrid(copy.deepcopy(grid1))
    for i in range(17, 21):
        if i == 17:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid1))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid2 = mirrorGrid(copy.deepcopy(grid2))
    for i in range(21, 25):
        if i == 21:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid2))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid3 = mirrorGrid(copy.deepcopy(grid3))
    for i in range(25, 29):
        if i == 25:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid3))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    mirroredGrid4 = mirrorGrid(copy.deepcopy(grid4))
    for i in range(29, 33):
        if i == 29:
            grids[i] = rotateGrid(copy.deepcopy(mirroredGrid4))
        else:
            grids[i] = rotateGrid(copy.deepcopy(grids[i-1]))
    return Entity(name, grids)

def isNeighbour(cell1, cell2):
    cell1Row = cell1[0]
    cell1Column = cell1[1]
    cell2Row = cell2[0]
    cell2Column = cell2[1]
    
    if abs(cell1Row - cell2Row) not in [0,1] or abs(cell1Column - cell2Column) not in [0,1]:
        return False
    return True
    
def getNeighbours(cell):
    neighbours = []
    row = cell[0]
    column = cell[1]
    for rowOffset in range(-1, 2):
        for colOffset in range(-1, 2):
            if rowOffset != 0 or colOffset != 0:
                neighbours.append((row+rowOffset, column+colOffset))
    return neighbours
    
def getOnNeighbours(cell, grid):
    neighbours = 0
    row = cell[0]
    column = cell[1]
    for rowOffset in range(-1, 2):
        for colOffset in range(-1, 2):
            if rowOffset != 0 or colOffset != 0:
                neighbours += (grid[row+rowOffset][column+colOffset] == 1)
    return neighbours      

def applyRules(grid, row, column, state, neighbours):
    if state == ON:
        if neighbours not in [2,3]:
            grid[row][column] = OFF
    else:
        if neighbours == 3:
            grid[row][column] = ON
            
def checkEntities(grid, row, column, entites, entitiesCount):
    cellsChecked = []
    entityFound = False
    for entity in entites:
        if entityFound:
            break
        for entityMode in entity.grid:
            if entity.grid[entityMode] == ([col[column-1:column+(len(entity.grid[entityMode][0])-1)] for col in grid[row-1:row+(len(entity.grid[entityMode])-1)]]):
                entitiesCount[entity.name] += 1
                for i in range(0, len(entity.grid[entityMode])-2):
                    for j in range(0, len(entity.grid[entityMode][0])-2):
                        cell = (row+i, column+j)
                        cellsChecked.append(cell)
                entityFound = True
                break
    return cellsChecked

def checkOtherEntities(grid, checkedCells, cellsOn):
    entities = 0
    cells = set()
    for cell in cellsOn:
        if cell not in checkedCells:
            if cell not in cells:
                entities += 1
            cells.add(cell)
            cells.update(getNeighbours(cell))
    return entities

def makeSim(grid, width, height):
    grid.insert(0, [0 for i in range(len(grid[0])+2)])
    grid.append([0 for i in range(len(grid[0])+2)])
    for row in grid:
        row.insert(0, 0)
        row.append(0)
    nextGrid = copy.deepcopy(grid)
    entities = []

    entities.append(createBlockEntity())
    entities.append(createBeehiveEntity())
    entities.append(createLoafEntity())
    entities.append(createBoatEntity())
    entities.append(createTubEntity())
    entities.append(createBlinkerEntity())
    entities.append(createToadEntity())
    entities.append(createBeaconEntity())
    entities.append(createGliderEntity())
    entities.append(createLightWeightSpaceshipEntity())

    entitiesCount = {"block": 0,
                "beehive": 0,
                "loaf": 0,
                "boat": 0,
                "tub": 0,
                "blinker": 0,
                "toad": 0,
                "beacon": 0,
                "glider": 0,
                "lightWeightSpaceship": 0}
    entitiesCount = {entity: 0 for entity in entitiesCount}
    simulation(grid, nextGrid, width, height, entities, entitiesCount)
    grid = copy.deepcopy(nextGrid)
    grid.pop(0)
    grid.pop(-1)
    for row in grid:
        row.pop(0)
        row.pop(-1)
    return {"grid": grid, "entities": entitiesCount}

ON = 1
OFF = 0
            