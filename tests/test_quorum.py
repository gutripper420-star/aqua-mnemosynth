import pytest

from backend import quorum as q


def test_fault_bound_matches_supplied_f():
    assert q.max_faults(q.TOTAL_NODES_N) == q.MAX_MALICIOUS_F == 242


def test_classic_case_n_equals_3f_plus_1():
    assert q.min_safe_quorum(7) == 5 and q.min_safe_quorum(727) == 485


def test_supplied_threshold_is_not_safe_for_n_729():
    # 485 is correct for N = 727; for N = 729 two quorums may overlap in only 241 < f + 1 nodes
    assert 2 * q.SUPPLIED_THRESHOLD_Q - q.TOTAL_NODES_N == 241
    assert not q.is_safe_quorum(q.SUPPLIED_THRESHOLD_Q, q.TOTAL_NODES_N)
    assert q.min_safe_quorum(q.TOTAL_NODES_N) == 486
    assert q.is_safe_quorum(486, q.TOTAL_NODES_N)


def test_has_quorum_boundaries():
    assert not q.has_quorum(485) and q.has_quorum(486)
    with pytest.raises(ValueError):
        q.has_quorum(730)
