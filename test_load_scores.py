from pathlib import Path

import pytest

from load_scores import load_scores


HERE = Path(__file__).resolve().parent


def test_배포된_성적표를_읽는다():
    kept, skipped = load_scores(HERE / "scores.csv")
    assert kept == [
        ("김하나", 88), ("최,네번", 77), ("김하나", 91),
        ("윤보람", 64), ("서한별", 95),
    ]
    assert [line for line, _, _ in skipped] == [3, 4, 7, 8, 9]


def test_빈_줄은_기록하지_않는다(tmp_path):
    path = tmp_path / "blank.csv"
    path.write_text("name,score\n가람,70\n\n나래,80\n", encoding="utf-8")
    assert load_scores(path) == ([("가람", 70), ("나래", 80)], [])


def test_따옴표_안의_쉼표를_이름에_포함한다(tmp_path):
    path = tmp_path / "quoted.csv"
    path.write_text('name,score\n"김,가람",75\n', encoding="utf-8")
    assert load_scores(path) == ([("김,가람", 75)], [])


def test_없는_파일이면_FileNotFoundError(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_scores(tmp_path / "missing.csv")


def test_헤더만_있으면_빈_결과를_돌려준다():
    assert load_scores(HERE / "empty.csv") == ([], [])


@pytest.mark.parametrize(
    "score, valid",
    [(-1, False), (0, True), (1, True), (99, True), (100, True), (101, False)],
)
def test_점수_경계값(tmp_path, score, valid):
    path = tmp_path / "boundary.csv"
    path.write_text(f"name,score\n가람,{score}\n", encoding="utf-8")
    if valid:
        assert load_scores(path) == ([("가람", score)], [])
    else:
        assert load_scores(path) == ([], [(2, f"가람,{score}", "점수가 0~100 밖")])


def test_이름이_비어_있으면_건너뛴_줄로_기록한다(tmp_path):
    path = tmp_path / "blank-name.csv"
    path.write_text("name,score\n,90\n", encoding="utf-8")
    assert load_scores(path) == ([], [(2, ",90", "이름이 비어 있음")])
