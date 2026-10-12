"""plans.py -- which units to use for N = 2^k points, and what that costs.  Standard library only.

A plan is a list of unit names (see circuit.py), one for each group of address bits, lowest
bits first.  Its cost is counted here by formula; the tests compare these numbers with the
operations that the programs really perform.

Norms (what the caller wants in front of H x):
  'exact'  H x itself.  If the plan has halvings, N multiplications at the end remove the factor.
  'raw'    whatever comes out: H x divided by 2^h, h = the number of halving units in the plan.
  'ortho'  H x / sqrt(N).  N multiplications at the end, unless the factor is already 1/sqrt(N).
"""
from fractions import Fraction
from .circuit import unit

G_UNITS = ('B2', 'G4', 'G8')        # integers only, no halving
O_UNITS = ('B2', 'O4', 'O8')        # the 4- and 8-point units halve once


def textbook_count(k):
    return k << k


def formula_pow8(j):
    """Count (O), exact H x, N = 8^j: 20 j 8^(j-1) + 8^j.  (The statement checked by Lean.)"""
    return (20 * j * 8 ** (j - 1) if j else 0) + 8 ** j


def formula_layers_O(k):
    """Count (O), exact H x, k = 3m + r: m layers of the 20-operation circuit, r textbook
    layers, N multiplications.  N (k - m/2 + 1); for m = 0 it is the textbook, N k."""
    m, n = k // 3, 1 << k
    return k * n if m == 0 else n * (2 * k - m + 2) // 2


def formula_family_G(k):
    """Count (G), the family: (3/4) N k + N/4 for k >= 2."""
    n = 1 << k
    return {0: 0, 1: 2}.get(k, (3 * n * k + n) // 4)


def alman_rao_exact(k):
    """Alman and Rao (2023), the exact count in the proof of their Theorem 6.2."""
    n = 1 << k
    return Fraction(23 * n * k, 24) + Fraction(n * (k % 3), 24) + n - 1


def published_G(k):
    """The count of Coppersmith, Feig and Linzer (1994, page 969): (7/8) N log2 N when N is a
    power of four, 7 operations on each pair of address bits, and (7/8) N log2 N + N/8 when N is
    an odd power of two, which is one textbook layer more.  Both formulas are theirs; the paper
    prints the formulas and the 7 at 4 points, and the other numbers are computed from them."""
    n = 1 << k
    return (k // 2) * 7 * n // 4 + (k % 2) * n


def layers_plan(k):
    """The 8-point unit on three bits at a time, a textbook step for each bit left over."""
    return ['O8'] * (k // 3) + ['B2'] * (k % 3)


def plan_factor(plan):
    f = Fraction(1)
    for u in plan:
        f *= unit(u).factor
    return f


def plan_cost(plan, count='O', norm='exact'):
    """Operations of a plan on N = 2^(its bits) points, final multiplications included."""
    k = sum(unit(u).bits for u in plan)
    n = 1 << k
    cost = 0
    for u in plan:
        c = unit(u)
        cost += (c.G if count == 'G' else c.O) * (n >> c.bits)
    if count == 'O':
        f = plan_factor(plan)
        if norm == 'exact' and f != 1:
            cost += n
        elif norm == 'ortho' and f * f * n != 1:
            cost += n
    return cost


def _compositions(k, units):
    """Every multiset of units that covers k bits, as a sorted list (largest units first)."""
    out = []

    def rec(left, start, acc):
        if left == 0:
            out.append(list(acc))
            return
        for t in range(start, len(units)):
            b = unit(units[t]).bits
            if b <= left:
                acc.append(units[t])
                rec(left - b, t, acc)
                acc.pop()
    rec(k, 0, [])
    return out


def best_plan(k, count='O', norm='exact'):
    """The cheapest mix of 8-point, 4-point and 2-point units for 2^k points.
    Ties go to the plan with the fewest units that are not textbook steps.  So when the
    textbook is as cheap as anything, the textbook is returned."""
    units = tuple(reversed(G_UNITS if count == 'G' else O_UNITS))
    best = None
    for p in _compositions(k, units):
        key = (plan_cost(p, count, norm), sum(1 for u in p if u != 'B2'))
        if best is None or key < best[0]:
            best = (key, p)
    return best[1] if best else []


def table(kmax=12):
    """Rows of the counts table: one dict for each k from 1 to kmax."""
    rows = []
    for k in range(1, kmax + 1):
        rows.append(dict(
            k=k, N=1 << k, textbook=textbook_count(k),
            G_published=published_G(k),
            G_family=formula_family_G(k),
            G_layers=plan_cost(best_plan(k, 'G'), 'G'),
            O_alman_rao=alman_rao_exact(k),
            O_layers=formula_layers_O(k),
            O_best=plan_cost(best_plan(k, 'O', 'exact'), 'O', 'exact'),
            O_raw=plan_cost(best_plan(k, 'O', 'raw'), 'O', 'raw'),
            O_ortho=plan_cost(best_plan(k, 'O', 'ortho'), 'O', 'ortho'),
        ))
    return rows
