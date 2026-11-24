from pathlib import Path

import pandas as pd


DATA_DIR = Path(__file__).resolve().parent


def 불러오기(경로):
    try:
        return pd.read_csv(경로, dtype={"학번": str})
    except UnicodeDecodeError:
        return pd.read_csv(경로, encoding="cp949", dtype={"학번": str})


def 정제(df):
    print("시작", len(df))
    df = df.dropna(subset=["점수"])
    print("빈 칸 제거", len(df))
    df = df.drop_duplicates().copy()
    print("중복 제거", len(df))
    df["반"] = df["반"].str.strip()
    df["과목"] = df["과목"].str.strip()
    print("공백 제거", len(df))
    df = df.loc[df["점수"].between(0, 100)].copy()
    print("범위 밖 제거", len(df))
    return df


def 반별평균(df):
    return df.groupby("반")["점수"].mean()


def main():
    원본 = 불러오기(DATA_DIR / "scores_2026.csv")
    df = 정제(원본)
    수학 = df.loc[df["과목"] == "수학"]
    print("\n수학 점수 행 수", len(수학))
    print("\n반별 평균\n", 반별평균(df).round(2).to_string())
    print("\n과목 × 반 통계\n",
          df.groupby(["과목", "반"])["점수"].agg(["count", "mean"]).round(2).to_string())
    그룹 = df.groupby("반")["점수"]
    통계 = 그룹.agg(개수="count", 평균="mean", 중앙값="median", 최댓값="max")
    print("\n반별 통계\n", 통계.round(2).to_string())
    print("\n그룹 합과 전체 합", 그룹.sum().sum(), df["점수"].sum())
    print("그룹 개수의 합과 전체 행 수", 그룹.count().sum(), len(df))
    점수 = 수학.loc[수학["반"] == "1반", "점수"]
    print("1반 수학 스팟 체크", 점수.tolist(), 점수.mean())


if __name__ == "__main__":
    main()
