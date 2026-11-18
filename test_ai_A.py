import pytest

from load_scores import load_scores


def test_missing_file_raises_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_header_only_returns_empty_lists(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text("이름,점수\n", encoding="utf-8")

    assert load_scores(path) == ([], [])


def test_keeps_valid_scores_in_order_including_duplicate_names(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "이름,점수\n"
        "  민수  , 0 \n"
        "지우,55\n"
        "민수,100\n",
        encoding="utf-8-sig",
    )

    assert load_scores(path) == (
        [("민수", 0), ("지우", 55), ("민수", 100)],
        [],
    )


@pytest.mark.parametrize(
    ("raw_line", "reason"),
    [
        pytest.param("민수", "열 개수가 2가 아님", id="one-column"),
        pytest.param("민수,50,추가", "열 개수가 2가 아님", id="three-columns"),
        pytest.param("민수,", "점수가 비어 있음", id="empty-score"),
        pytest.param("민수,   ", "점수가 비어 있음", id="whitespace-score"),
        pytest.param("민수,오십", "점수가 정수가 아님", id="text-score"),
        pytest.param("민수,50.5", "점수가 정수가 아님", id="decimal-score"),
        pytest.param("민수,-1", "점수가 0~100 밖", id="below-minimum"),
        pytest.param("민수,101", "점수가 0~100 밖", id="above-maximum"),
        pytest.param(",50", "이름이 비어 있음", id="empty-name"),
        pytest.param("   ,50", "이름이 비어 있음", id="whitespace-name"),
    ],
)
def test_records_invalid_row(tmp_path, raw_line, reason):
    path = tmp_path / "scores.csv"
    path.write_text(f"이름,점수\n{raw_line}\n", encoding="utf-8")

    assert load_scores(path) == ([], [(2, raw_line, reason)])


def test_ignores_blank_lines_and_preserves_skipped_row_numbers(tmp_path):
    path = tmp_path / "scores.csv"
    path.write_text(
        "이름,점수\n"
        "\n"
        "민수,\n"
        "지우,75\n"
        "\n"
        "하나,101\n"
        "서준,80\n",
        encoding="utf-8",
    )

    assert load_scores(path) == (
        [("지우", 75), ("서준", 80)],
        [
            (3, "민수,", "점수가 비어 있음"),
            (6, "하나,101", "점수가 0~100 밖"),
        ],
    )
