from typing import List, Set, Tuple
from CSP.Constraint import Constraint
from CSP.Variable import Variable


class NonogramConstraint(Constraint):
    """
    Constraint for a Nonogram puzzle row or column.
    Checks if the sequence of filled cells matches the given clue.
    Optimized with line-solving techniques.
    """

    def __init__(self, variables: List[Variable], clue: List[int]):
        """
        Args:
            variables: List of variables representing a row or column
            clue: List of integers indicating consecutive filled cells
                  e.g., [2, 3] means 2 filled cells, then 3 filled cells with at least 1 gap
        """
        super().__init__(variables)
        self.clue = clue
        # length of rows or columns
        self.line_length = len(self.variables)

        if not self.clue:
            # when there are no clue , no space is needed
            self.min_length = 0
        else:
            # number of the cells that should be filled + the number of gap (minimum gap = 1)
            self.min_length = sum(self.clue) - (len(self.clue) - 1)

    def is_satisfied(self) -> bool:
        """
        Check if the current assignment satisfies the nonogram constraint.
        Returns True if all variables are assigned and match the clue,
        or if not all variables are assigned yet (partial consistency check).
        """
        # Get the values of all variables (None if unassigned, 0 or 1 if assigned)
        values = [var.value for var in self.variables]

        # If not all variables are assigned, check partial consistency
        if None in values:
            return self._is_partially_consistent(values)

        # All variables assigned - check full consistency
        return self._matches_clue(values)

    def _is_partially_consistent(self, values: List[int]) -> bool:
        """
        Check if a partial assignment could potentially satisfy the constraint.
        This allows for early pruning during search.
        Optimized version with better pruning.
        """
        if not self.clue:
            # Empty clue - no filled cells allowed
            return all(v != 1 for v in values)

        assigned_filled = sum(1 for v in values if v == 1)
        real_filled = sum(self.clue)
        unassigned = sum(1 for v in values if v is None)

        # if the cells that assigned 1 is more that total 1 in clue
        # we'll never be able to assigned it like this in real problem
        if assigned_filled > real_filled:
            return False

        # we'll have maximum number of 1 if all the None in values are assigned 1
        # if the maximum is less that number on 1 inn clue then ww can never reach the clue
        if assigned_filled+unassigned < real_filled:
            return False

        assigned_blocks = self._count_blocks(values)

        # if the minimum length of each block is greater that maximum length of blocks in clue
        # then it be always greater, and it's not satisfy the constraints
        # index of blocks might change depend on how we assign None
        # That's why we just check it with the maximum
        max_clue = max(self.clue)
        if any(b > max_clue for b in assigned_blocks):
            return False

        # if it satisfies all the above conditions
        # then we'll might be on right path
        return True
    pass

    @staticmethod
    def _count_blocks(values: List[int]) -> List[int]:

        # checks if the values has the same block of 1 as clue
        block_length = 0
        check = []
        for i in range(len(values)):
            if values[i] == 0 and not block_length == 0:
                check.append(block_length)
                block_length = 0
            elif values[i] == 1:
                block_length += values[i]

        if not block_length == 0:
            check.append(block_length)

        return check

    pass
    def _matches_clue(self, values: List[int]) -> bool:
        """
        Check if a complete assignment matches the clue exactly.
        """
        if self._count_blocks(values) == self.clue:
            return True

        return False

    pass
