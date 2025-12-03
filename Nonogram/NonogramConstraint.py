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
        # طول سطر/ستون
        self.line_length = len(self.variables)  # TODO: Implemented
        # حداقل طول لازم برای جا شدن همه بلوک‌ها + فاصله‌های اجباری
        if not self.clue:
            self.min_length = 0  # هیچ بلوکی نداریم
        else:
            self.min_length = sum(self.clue) + (len(self.clue) - 1)  # TODO: Implemented

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
        # مقدار None: هنوز مشخص نیست
        # مقدار 0 : خانه خالی
        # مقدار 1 : خانه پر

        # اگر هیچ بلوکی در clue نیست، نباید هیچ 1ای وجود داشته باشد
        if not self.clue:
            return all(v != 1 for v in values)

        n = len(values)

        # ۱) اگر تعداد ۱های فعلی از مجموع سرنخ‌ها بیشتر باشد → غیرممکن
        total_filled_now = sum(1 for v in values if v == 1)
        total_required = sum(self.clue)
        if total_filled_now > total_required:
            return False

        # ۲) اگر حتی با پر کردن همه Noneها، به حداقل طول لازم نمی‌رسیم → غیرممکن
        max_possible_filled = total_filled_now + sum(1 for v in values if v is None)
        if max_possible_filled < total_required:
            return False

        # ۳) بررسی نکند که هیچ بلوک فعلی طولش از سرنخ متناظر بیشتر شده باشد
        # تبدیل رشته به گروه‌های متوالی از ۱ و طولشان
        segments = []
        count = 0
        for v in values:
            if v == 1:
                count += 1
            else:
                if count > 0:
                    segments.append(count)
                    count = 0
        if count > 0:
            segments.append(count)

        # اگر تعداد گروه‌های ۱ فعلی بیشتر از تعداد بلوک‌ها باشد → غیرممکن
        if len(segments) > len(self.clue):
            return False

        # هیچ سگمنت نباید از بلوک متناظر خودش بزرگ‌تر باشد
        for i, seg_len in enumerate(segments):
            if seg_len > self.clue[i]:
                return False

        # اگر تازه داریم بلوک‌ها را شروع می‌کنیم یا بینشان هستیم،
        # امکان ادامه دادن وجود دارد، پس در اینجا می‌گوییم می‌تواند سازگار باشد
        return True

    def _matches_clue(self, values: List[int]) -> bool:
        """
        Check if a complete assignment matches the clue exactly.
        """
        # استخراج طول بلوک‌های متوالی از ۱ها
        segments = []
        count = 0
        for v in values:
            if v == 1:
                count += 1
            else:
                if count > 0:
                    segments.append(count)
                    count = 0
        if count > 0:
            segments.append(count)

        # باید دقیقا با clue برابر باشد
        return segments == self.clue
