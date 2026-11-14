"""Byzantine quorum arithmetic for an N-node network.

Only thresholds are implemented; there is no networking or consensus protocol.
Tolerating f faults needs N >= 3f + 1. A quorum Q is safe if any two quorums
overlap in at least f + 1 nodes (so one is honest): 2Q - N >= f + 1, hence
Q >= ceil((N + f + 1) / 2). For N = 3f + 1 this equals 2f + 1.
"""

TOTAL_NODES_N = 729
MAX_MALICIOUS_F = 242
SUPPLIED_THRESHOLD_Q = 485  # author-supplied value; see is_safe_quorum


def max_faults(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    return (n - 1) // 3


def min_safe_quorum(n: int, f: int | None = None) -> int:
    f = max_faults(n) if f is None else f
    return (n + f + 2) // 2  # ceil((n + f + 1) / 2)


def is_safe_quorum(q: int, n: int, f: int | None = None) -> bool:
    return q >= min_safe_quorum(n, f) and q <= n - (max_faults(n) if f is None else f)


def has_quorum(votes: int, n: int = TOTAL_NODES_N) -> bool:
    if not 0 <= votes <= n:
        raise ValueError("votes must be between 0 and n")
    return votes >= min_safe_quorum(n)
