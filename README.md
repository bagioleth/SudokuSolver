# SudokuSolver

In order to solve a sudoku board, this program uses a stack to store the game states as it is solving. When there are more than 1 possible value for a square, the solver pushes all possible board states to the stack. If a board gets to a state where no empty square can be filled without being invalid, the board is poped from the stack and forgotten. When there are no boards on the stack, the puzzle is not solvable

Sudoku Solver uses 2 methods to solve a sudoku puzzle.

solvePuzzleDegree tries to solve the squares with the most possible values first. This leads to more branching of possible board states early on.

solvePuzzleMinimum tries to solves the squares with the least possible values first. This leads to less branching early and is more akin to how humans solve sudoku.

After running some tests, it was determined that solvePuzzleMinimum was a more practical way of solving the puzzle