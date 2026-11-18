# 성적 CSV 검사 프로그램

## ① 무엇을 하나요

성적 CSV에서 유효한 이름과 점수를 읽고, 건너뛴 데이터의 줄 번호와 이유를 기록합니다.

## ② 왜 만들었나요

성적 CSV에는 빈 점수, 숫자가 아닌 값, 범위를 벗어난 점수가 섞여 있습니다. 유효한 성적은 계속 읽고, 제외된 행은 나중에 확인할 수 있도록 줄 번호와 이유를 남기기 위해 만들었습니다.

## ③ 어떻게 쓰나요

Python 3이 설치된 환경에서 이 저장소 폴더를 열고 실행합니다.

```bash
python3 load_scores.py scores.csv
```

정상적으로 실행되면 유효한 줄 5개와 건너뛴 줄 5개가 출력됩니다. 같은 이름이 나와도 각각 보존합니다. `empty.csv` 또는 `weird.csv`로 파일명을 바꿔 다른 입력도 확인할 수 있습니다.

## ④ 어떻게 테스트하나요

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install pytest pytest-cov
python -m pytest -q
python -m pytest -q --cov=load_scores --cov-report=term-missing test_load_scores.py
```

실제 전체 테스트 실행 출력 (macOS, Python 3.14.7)

```text
......................................                                   [100%]
38 passed in 0.03s
```

의도적으로 고장난 `find_max`의 함정 실험을 실행하려면 `python -m pytest -q test_ai_bug.py`를 사용합니다. 마지막 원소가 최댓값인 두 케이스가 실패합니다.

## ⑤ 파일 구성

| 파일 | 하는 일 |
| --- | --- |
| `load_scores.py` | 성적 CSV를 읽는 함수와 터미널 실행 코드 |
| `scores.csv`, `empty.csv`, `weird.csv` | 일반, 헤더만 있는 경우, 잘못된 행이 섞인 예제 |
| `test_load_scores.py` | 설계표 기반 테스트와 커버리지 확인 후 추가한 테스트 |
| `test_ai_A.py`, `test_ai_B.py` | 코드 중심 조건과 명세 중심 조건을 재현한 비교 테스트 |
| `bug3_logic.py`, `test_ai_bug.py` | 배포된 논리 오류 예제와 함정 테스트 |
| `pytest.ini` | 기본 실행에는 성적 CSV 테스트 세 파일만 포함 |
| `prompts.txt` | 수업에서 배포한 실험 프롬프트 |
| `LICENSE` | MIT 라이선스 문구 |

## ⑥ 만든 사람 · AI를 어디에 썼는지

- 만든 사람 — @comjessi (GitHub 제출 계정)
- AI를 쓴 곳 — OpenAI Codex로 테스트와 문서 초안을 작성하고 실행 결과를 기록했습니다. A·B·함정 실험은 동일한 모델과 설정으로 독립된 Codex 대화 세 개에서 각각 진행했습니다. B에는 11주차 배포본의 요약을 바탕으로 재구성한 명세를 사용했습니다.
- 결과 확인 — 0점과 100점은 유효하고 101점은 제외되는지 확인했습니다. 이 항목은 Codex가 수행한 검증을 기록합니다.

## 라이선스

MIT License. 원본 배포 파일의 출처는 AI 협업 프로그래밍 11주차 실습 자료입니다.
