import pytest

from load_scores import load_scores


def write_csv(tmp_path, contents):
    path = tmp_path / "scores.csv"
    path.write_text(contents, encoding="utf-8")
    return path


def test_keeps_utf8_names_quoted_commas_duplicates_and_boundary_scores(tmp_path):
    path = write_csv(
        tmp_path,
        'name,score\n'
        '민지,0\n'
        '"김,하늘",100\n'
        '민지,42\n'
        '민지,42\n',
    )

    assert load_scores(path) == (
        [("민지", 0), ("김,하늘", 100), ("민지", 42), ("민지", 42)],
        [],
    )


def test_header_only_returns_empty_lists(tmp_path):
    path = write_csv(tmp_path, "name,score\n")

    assert load_scores(path) == ([], [])


def test_missing_file_propagates_file_not_found_error(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


@pytest.mark.parametrize(
    "invalid_row",
    [
        pytest.param("민지", id="too-few-columns"),
        pytest.param("민지,50,extra", id="too-many-columns"),
        pytest.param(",50", id="empty-name"),
        pytest.param("민지,", id="empty-score"),
        pytest.param("민지,abc", id="non-numeric-score"),
        pytest.param("민지,50.5", id="fractional-score"),
        pytest.param("민지,-1", id="below-minimum"),
        pytest.param("민지,101", id="above-maximum"),
    ],
)
def test_records_invalid_row_and_keeps_surrounding_valid_rows(tmp_path, invalid_row):
    path = write_csv(tmp_path, f"name,score\n하늘,25\n{invalid_row}\n지수,75\n")

    kept, skipped = load_scores(path)

    assert kept == [("하늘", 25), ("지수", 75)]
    assert len(skipped) == 1
    line_number, original_line, reason = skipped[0]
    assert line_number == 3
    assert original_line.rstrip("\r\n") == invalid_row
    # 사유의 구체적인 문구는 명세에 정해져 있지 않다.
    assert isinstance(reason, str) and reason.strip()


def test_blank_lines_are_unrecorded_and_count_toward_line_numbers(tmp_path):
    path = write_csv(tmp_path, "name,score\n\n민지,101\n\n하늘,50\n지수,\n\n")

    kept, skipped = load_scores(path)

    assert kept == [("하늘", 50)]
    assert [
        (line_number, original_line.rstrip("\r\n"))
        for line_number, original_line, _ in skipped
    ] == [(3, "민지,101"), (6, "지수,")]
