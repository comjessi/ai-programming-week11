import pytest

from bug3_logic import find_max


@pytest.mark.parametrize(
    ("scores", "expected"),
    [
        pytest.param([90, 70, 80], 90, id="maximum-first"),
        pytest.param([70, 90, 80], 90, id="maximum-middle"),
        pytest.param([70, 80, 90], 90, id="maximum-last"),
        pytest.param([-9, -2, -5], -2, id="negative-scores"),
        pytest.param([80, 80, 80], 80, id="all-equal"),
        pytest.param([42], 42, id="single-score"),
        pytest.param([1, 2], 2, id="two-scores-ascending"),
        pytest.param([2, 1], 2, id="two-scores-descending"),
    ],
)
def test_find_max(scores, expected):
    assert find_max(scores) == expected


def test_find_max_empty_list_raises_index_error():
    with pytest.raises(IndexError):
        find_max([])
