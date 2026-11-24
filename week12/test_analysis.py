import pytest

from analysis import DATA_DIR, 반별평균, 불러오기, 정제


@pytest.fixture(scope="module")
def 본():
    return 정제(불러오기(DATA_DIR / "scores_2026.csv"))


def test_정제하면_100행이_남는다(본):
    assert len(본) == 100


def test_반은_두_종류만_남는다(본):
    assert sorted(본["반"].unique().tolist()) == ["1반", "2반"]


def test_그룹합이_전체합과_같다(본):
    그룹 = 본.groupby("반")["점수"]
    assert 그룹.sum().sum() == 본["점수"].sum()
    assert 그룹.count().sum() == len(본)


def test_손계산과_일치한다():
    미니 = 정제(불러오기(DATA_DIR / "mini.csv"))
    assert len(미니) == 7
    assert 반별평균(미니).to_dict() == {"1반": 80.0, "2반": 70.0}
