import networkx as nx


def createSudokuPuzzle():
    # Create a grid of size n
    G = nx.grid_2d_graph(2, 2)

    # Draw the graph using NetworkX and Matplotlib
    pos = {(x,y):(y,-x) for x,y in G.nodes()}

    # ADd Diagonal edges
    for (x, y) in G.nodes():

        if (x + 1 < 2) and (y + 1 < 2):
            G.add_edge((x, y), (x + 1, y + 1))  # add \ diagonal

        if (x + 1 < 2) and (y - 1 >= 0):
            G.add_edge((x, y), (x + 1, y - 1))


    return G

class EmptyIndex:

    def __init__(self, row, column) -> None:
        self.row = row
        self.column = column

    def __str__(self) -> str:
        return f'(Row: {self.row}; IndexInRow: {self.column})'
    
    def __repr__(self):
        return self.__str__()


class SudokuSolver:
    
    def QuantumSolve(sudokuPuzzle: nx.classes.graph.Graph):
        size = sudokuPuzzle
        
    def FindEdgesAndNumberConstraints(self, puzzle, size: int):
        
        subSize = 2 if size == 4 else 1
        emptyIndexes = [[0]*size for _ in range(size)]
        emptySquares = []
        emptyCellConstraints = []

        startingNumberConstraints = set()


        for i in range(size):

            for j in range(size):

                # Check if a cell is empty
                if puzzle[i][j] == 0:
                    # set the index of the empy cell found 
                    # First found empty cell would be 0 then 1 and so on
                    emptyIndex = len(emptySquares)
                    # Add the found cells index into the empty squares list
                    emptyIndexes[i][j] = emptyIndex
                    emptySquares.append(EmptyIndex(i, j))

                    # Find all existing Constraints in Subgrid, Diagonal and Horizontal

                    # This is the formula to find every subGrid within the sudoku
                    iSubGridStart = i // subSize * subSize
                    jSubGridStart = j // subSize * subSize
                    
                    # Check the box for any constraints
                    for iSub in range(iSubGridStart, i):

                        for jSub in range(jSubGridStart, j):
                            if puzzle[iSub][jSub] != 0:
                                startingNumberConstraints.add((emptyIndex, puzzle[iSub][jSub] - 1))
                            elif iSub < jSub and iSub != i and jSub != j:
                                emptyCellConstraints.append([emptyIndex, emptyIndexes[iSub][jSub]])

                    for ii in range(0, size):
                        if puzzle[ii][j] != 0:
                            startingNumberConstraints.add((emptyIndex, puzzle[ii][j] - 1))
                        elif ii < i:
                            emptyCellConstraints.append([emptyIndex, emptyIndexes[ii][j]])

                    for jj in range(0, size):
                        if puzzle[i][jj] != 0:
                            startingNumberConstraints.add((emptyIndex, puzzle[i][jj] - 1))
                        elif jj < j:
                            emptyCellConstraints.append([emptyIndex, emptyIndexes[i][jj]])

                    if size == 9:  # Invalidate numbers that are illegal on a 9x9 board
                        for invalid in range(9, 16):
                            startingNumberConstraints.add((emptyIndex, invalid))

        return emptyCellConstraints, startingNumberConstraints, emptySquares
















 

