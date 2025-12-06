from CSP.Solver import Solver, FastNonogramSolver
from States.StatesProblem import StatesProblem
from Nonogram.NonogramProblem import NonogramProblem  # add NonogramProblem

if __name__ == '__main__':
    # Solve the StatesProblem
    states = StatesProblem()
    s = Solver(states)
    s.solve()
    states.print_assignments()

    # solving the NonogramProblem (25x25 Dolphin)
    # Separate outputs for greater clarity
    print("\n--- Solving Nonogram (Dolphin 25x25) ---\n")
    nonogram = NonogramProblem()
    # using the fast solver for Nonogram
    s_nonogram = FastNonogramSolver(nonogram)
    s_nonogram.solve()
    nonogram.print_assignments()