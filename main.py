#TODO: use nonogram for testing here

from CSP.Solver import Solver, FastNonogramSolver
from States.StatesProblem import StatesProblem
from Nonogram.NonogramProblem import NonogramProblem  # اضافه کردن NonogramProblem

if __name__ == '__main__':
    # حل مسئله StatesProblem
    states = StatesProblem()
    s = Solver(states)
    s.solve()
    states.print_assignments()

    # حل مسئله NonogramProblem (25x25 Dolphin)
    print("\n--- Solving Nonogram (Dolphin 25x25) ---\n")  # جداسازی خروجی‌ها برای وضوح بیشتر
    nonogram = NonogramProblem()
    s_nonogram = FastNonogramSolver(nonogram)  # استفاده از Solver سریع برای نونوگرام
    s_nonogram.solve()
    nonogram.print_assignments()