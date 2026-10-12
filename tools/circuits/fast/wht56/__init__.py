"""wht56 -- the Walsh-Hadamard transform computed with circuits that use fewer operations
than the textbook's N log2 N.  The name is the rate of the main one: (5/6) N log2 N + N.

    from wht56 import wht, textbook, family, Tally      (pure Python, exact; reference.py)
    from wht56.fast import fwht                        (numpy; fast.py)
    python3 -m wht56 --selftest | --count K | --bench | --gen python|c|kernels --size N

README.md says what this is and what it is not.
"""
from .reference import (textbook, wht, layers8, layers8_half, layers8_int, family,
                        Tally, count, matrix_times)
from .plans import best_plan, layers_plan, plan_cost, table

__all__ = ['textbook', 'wht', 'layers8', 'layers8_half', 'layers8_int', 'family', 'Tally',
           'count', 'matrix_times', 'best_plan', 'layers_plan', 'plan_cost', 'table']
