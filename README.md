# 🛒 멀티모달 검색 & Multi-Stage 추천 시스템

텍스트·이미지로 상품을 검색(CLIP + FAISS)하고, 3단계 파이프라인(후보 생성 → 랭킹 → 리랭킹)으로 개인화 추천을 제공하는 이커머스 AI 프로젝트입니다.

---

## 📌 목차

1. [프로젝트 개요](#1-프로젝트-개요)
2. [빠른 시작](#2-빠른-시작)
3. [폴더 구조](#3-폴더-구조)
4. [팀 협업 규칙 (꼭 읽어주세요)](#4-팀-협업-규칙-꼭-읽어주세요)
5. [커밋 메시지 규칙](#5-커밋-메시지-규칙)
6. [브랜치 규칙](#6-브랜치-규칙)
7. [PR(풀 리퀘스트) 규칙](#7-pr풀-리퀘스트-규칙)
8. [팀 역할](#8-팀-역할)
9. [개발 진행 순서](#9-개발-진행-순서)

---

## 1. 프로젝트 개요

| 구분 | 내용 |
|---|---|
| 검색 | CLIP 임베딩 + FAISS 인덱스, 텍스트/이미지/혼합 검색 |
| 추천 | Two Tower(후보 생성) → DeepFM(랭킹) → 리랭킹(다양성, 신규상품, MAB) |
| 서빙 | FastAPI + Redis Feature Store |
| 대시보드 | Streamlit (검색 품질, 추천 성능, A/B 테스트) |
| 실행 환경 | Docker Compose (redis, api-server, dashboard, simulator) |

**주요 제약:** 외부 클라우드 API 사용 금지(로컬에서 모두 동작), 설정은 `config.yaml`로 관리, random seed 42 고정

---

## 2. 빠른 시작

### 처음 받는 팀원

```bash
# 1. 저장소 받기
https://github.com/k-pang-2026/k-pang.git
cd mm-recsys

# 2. 커밋 메시지 템플릿 적용 (최초 1회)
git config commit.template .gitmessage

# 3. 환경 변수 파일 만들기
cp .env.example .env

# 4. 파이썬 가상환경 + 패키지 설치
python -m venv .venv
source .venv/bin/activate          # Windows Git Bash: source .venv/Scripts/activate
pip install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# 5. 전체 시스템 실행
docker compose up --build
```

### 실행 확인

| 확인 | 주소 / 명령 |
|---|---|
| API 상태 | `curl localhost:8000/health` → `{"status":"ok"}` |
| API 문서 | http://localhost:8000/docs |
| 대시보드 | http://localhost:8501 |
| 테스트 | `python -m pytest -q tests` |

> `docker compose` 명령은 **`docker-compose.yml`이 있는 프로젝트 폴더 안에서** 실행해야 합니다.

---

## 3. 폴더 구조

```text
mm-recsys/
├── README.md                 # 지금 보고 있는 문서
├── config.yaml               # 모든 설정값 (하드코딩 금지!)
├── .env.example              # 환경변수 예시 (복사해서 .env 로 사용)
├── docker-compose.yml        # 컨테이너 4개 실행 설정
├── requirements.txt          # 파이썬 패키지 목록
├── docker/                   # Dockerfile 모음
├── docs/                     # 문서, 실험 리포트
├── data/                     # 데이터 (Git에 올리지 않음)
├── models/                   # 학습된 모델 (Git에 올리지 않음)
├── src/
│   ├── simulator/            # 고객 행동 시뮬레이터
│   ├── search/               # CLIP 임베딩, FAISS, BM25
│   ├── recommendation/       # Two Tower, DeepFM, 리랭킹, MAB
│   ├── serving/              # FastAPI, Redis Feature Store
│   ├── evaluation/           # 평가 지표, A/B 테스트
│   ├── ct/                   # 성능 모니터링, 재학습
│   └── common/               # 공통 설정 로더, seed
├── dashboard/                # Streamlit 대시보드
└── tests/                    # 테스트 코드
```

---

## 4. 팀 협업 규칙 (꼭 읽어주세요)

### 한눈에 보는 작업 흐름

```text
 ① main 최신화  →  ② 내 브랜치 만들기  →  ③ 작업 & 커밋  →  ④ 푸시  →  ⑤ PR 생성  →  ⑥ 리뷰  →  ⑦ Squash 머지
```

### 지켜야 할 약속 5가지

1. **`main` 브랜치에 직접 푸시하지 않습니다.** (막혀 있습니다)
2. 작업은 **항상 내 브랜치**에서 합니다.
3. 합칠 때는 **PR을 만들고 리뷰를 받습니다.**
4. 커밋 메시지는 **아래 규칙**대로 씁니다.
5. `data/`, `models/`, `.env`, `.venv/`는 **절대 올리지 않습니다.**

---

## 5. 커밋 메시지 규칙

### 5-1. 기본 모양

```text
타입(범위): 제목
```

> 영어 단어 하나 + 괄호 안에 작업 영역 + 콜론 + 한글 제목

**예시**

```text
feat(search): CLIP 검색 API 구현
fix(serving): Redis 연결 오류 수정
docs: README 작성
```

### 5-2. 타입 — "무슨 종류의 작업인가요?"

| 타입 | 언제 쓰나요? | 예시 |
|---|---|---|
| `feat` | 새 기능을 **만들었을 때** | `feat(simulator): 페르소나 6종 생성기 추가` |
| `fix` | 버그를 **고쳤을 때** | `fix(search): nprobe 설정이 적용되지 않는 문제 수정` |
| `docs` | **문서**만 고쳤을 때 | `docs: A/B 테스트 리포트 작성` |
| `refactor` | 동작은 같고 **코드 구조만 정리**했을 때 | `refactor(recommend): 리랭킹을 전략 패턴으로 분리` |
| `test` | **테스트 코드**를 추가/수정했을 때 | `test(eval): 지표 계산 테스트 추가` |
| `chore` | 설정, 도커, 패키지 등 **환경 작업** | `chore(docker): .dockerignore 추가` |
| `perf` | **속도를 개선**했을 때 | `perf(search): nprobe 조정으로 응답시간 단축` |
| `style` | 코드 모양(띄어쓰기 등)만 바꿨을 때 | `style: 포맷 정리` |

### 5-3. 범위 — "어느 폴더를 건드렸나요?"

| 범위 | 대상 폴더/파일 |
|---|---|
| `simulator` | `src/simulator/` |
| `search` | `src/search/` |
| `recommend` | `src/recommendation/` |
| `serving` | `src/serving/` (API, Redis) |
| `eval` | `src/evaluation/` |
| `ct` | `src/ct/` |
| `dashboard` | `dashboard/` |
| `docker` | `docker/`, `docker-compose.yml` |
| `config` | `config.yaml`, `.env.example` |
| `docs` | `docs/`, README |

여러 곳을 건드렸다면 범위를 **생략**해도 됩니다. 예: `chore: 개발환경 초기 세팅`

### 5-4. 작성 요령

- 제목은 **50자 이내**, 끝에 마침표 없이 씁니다.
- 제목은 **"~추가", "~수정", "~구현"** 처럼 끝맺음을 통일합니다.
- **한 커밋에는 한 가지 일만** 담습니다.
- 필요하면 빈 줄 뒤에 **왜 바꿨는지, 성능 수치**를 본문에 적습니다.

```text
feat(search): CLIP + FAISS 검색 API 구현

- /api/search 에서 text / image / hybrid 지원
- dev 스케일 기준 MRR 0.58, p95 120ms
```

### 5-5. 좋은 예 vs 나쁜 예

| ✅ 좋은 예 | ❌ 나쁜 예 | 왜 나쁜가요? |
|---|---|---|
| `feat(recommend): Two Tower 후보 생성 모델 구현` | `수정` | 무엇을 수정했는지 모름 |
| `fix(serving): Redis 장애 시 빈 피처로 폴백` | `update` | 내용 없음 |
| `perf(search): nprobe 16→8, p95 180→95ms` | `asdf` | 의미 없음 |
| `docs: A/B 테스트 리포트 작성` | `여러가지 고침` | 한 커밋에 너무 많은 일 |

### 5-6. 커밋 템플릿 사용하기

처음 한 번만 설정하면 `git commit` 입력 시 안내 문구가 자동으로 나옵니다.

```bash
git config commit.template .gitmessage
```

---

## 6. 브랜치 규칙

### 6-1. 브랜치가 뭔가요?

`main`은 **"항상 잘 돌아가야 하는 완성본"** 입니다. 각자 **복사본(브랜치)** 에서 작업하고, 검토가 끝나면 `main`에 합칩니다.

```text
main    ●───────●───────────●────────●
         \                 /
내 브랜치  ●──●──●──●──●──●   (작업 후 PR로 합침)
```

### 6-2. 브랜치 이름 짓기

```text
타입/작업-내용
```

| 접두사 | 용도 | 예시 |
|---|---|---|
| `feat/` | 새 기능 개발 | `feat/simulator`, `feat/search-api` |
| `fix/` | 버그 수정 | `fix/faiss-nprobe` |
| `docs/` | 문서 작업 | `docs/readme`, `docs/ab-report` |
| `chore/` | 환경/설정 작업 | `chore/docker-fix` |

**이름 규칙**
- 영어 소문자와 하이픈(`-`)만 씁니다. (띄어쓰기, 한글 ❌)
- 무슨 작업인지 알아볼 수 있게 짓습니다. (`test1`, `my-branch` ❌)

### 6-3. 기능별 브랜치 예시

| 브랜치 | 작업 내용 |
|---|---|
| `feat/simulator` | 고객 행동 시뮬레이터 |
| `feat/search-api` | CLIP, FAISS, 검색 API |
| `feat/two-tower` | 후보 생성 모델 |
| `feat/deepfm-ranking` | 랭킹 모델, 추천 API |
| `feat/reranking-mab` | 리랭킹, MAB, 세션 추천 |
| `feat/feature-store` | Redis Feature Store |
| `feat/ab-test` | A/B 테스트 |
| `feat/dashboard` | 대시보드 |
| `feat/ct-pipeline` | 재학습 파이프라인 |
| `docs/reports` | 리포트 작성 |

### 6-4. 브랜치 사용 흐름 (복사해서 쓰세요)

```bash
# ① main 최신 상태로 맞추기
git checkout main
git pull origin main

# ② 내 브랜치 만들기
git checkout -b feat/simulator

# ③ 작업 후 커밋
git add src/simulator/
git commit              # 템플릿이 뜨면 규칙대로 작성

# ④ 내 브랜치를 GitHub에 올리기
git push -u origin feat/simulator

# ⑤ GitHub 에서 PR 만들기 (아래 7번 참고)
```

### 6-5. 브랜치 작업 팁

- **오래 끌지 마세요.** 며칠씩 지속하면 다른 사람과 충돌이 커집니다. 큰 작업은 쪼개서 자주 합치세요.
- 작업 중에 `main`이 바뀌었으면 받아 옵니다.
  ```bash
  git fetch origin
  git merge origin/main
  ```
- 머지가 끝난 브랜치는 **자동 삭제**됩니다. 로컬에서도 지웁니다.
  ```bash
  git checkout main && git pull origin main
  git branch -d feat/simulator
  ```

### 6-6. 충돌이 나기 쉬운 공용 파일

| 파일 | 조심할 점 |
|---|---|
| `config.yaml`, `requirements.txt` | 내 것을 **추가만** 하고, 남의 줄은 건드리지 않기 |
| `src/serving/main.py` | 가능하면 라우터 파일을 따로 만들어 수정하기 |
| `src/common/` | 수정 전에 **팀에 먼저 공유** |
| 데이터 컬럼명(스키마) | 시뮬레이터 작업 시작 전에 **팀이 합의하고 고정** |

---

## 7. PR(풀 리퀘스트) 규칙

**PR = "내 브랜치를 main에 합쳐도 될까요?" 라는 요청서**입니다.

### 7-1. PR 만드는 법

1. 브랜치를 푸시하면 GitHub에 **Compare & pull request** 버튼이 뜹니다. 클릭합니다.
2. **제목**은 커밋 규칙과 똑같이 씁니다. (이 제목이 `main`의 기록이 됩니다)
   ```text
   feat(simulator): 행동 로그 생성기 구현
   ```
3. **본문**은 자동으로 채워지는 템플릿에 맞춰 작성합니다.
   - 무엇을, 왜 바꿨는지
   - 어떻게 테스트했는지
   - 성능 수치(있다면)
4. 오른쪽 **Reviewers**에서 리뷰할 팀원을 지정합니다.

### 7-2. 리뷰 & 머지 규칙

| 항목 | 규칙 |
|---|---|
| 머지 전 리뷰 | **최소 1회 이상** (작성자 본인 자체 점검 포함) |
| 리뷰 기한 | 요청 후 **24시간 이내** 확인 |
| PR 크기 | **300줄 안팎**으로 작게 |
| 머지 방식 | **Squash and merge** (PR 전체가 커밋 1개로 합쳐짐) |
| 머지 후 | 브랜치 자동 삭제 |

> 💡 GitHub는 **본인이 만든 PR을 본인이 Approve할 수 없습니다.** 그래서 "승인 필수" 설정은 0으로 두고, **리뷰 코멘트를 남긴 뒤 머지**하는 것을 팀 약속으로 합니다. 팀원이 늘면 "다른 사람 승인 1명"으로 올립니다.

### 7-3. 리뷰어가 확인할 것

- [ ] `.venv`, `data/`, `models/`, `.env` 같은 **불필요한 파일**이 없는가
- [ ] 설정값을 코드에 **하드코딩**하지 않고 `config.yaml`을 썼는가
- [ ] 함수에 **타입힌트**가 있는가
- [ ] **데이터 누수**(미래 정보로 학습)나 **seed 미고정**은 없는가
- [ ] `pytest`가 통과하는가

---

## 8. 팀 역할

| 이름 | 역할 | 담당 영역 |
|---|---|---|
| (이름) | (예: 시뮬레이터) | `src/simulator/` |
| (이름) | (예: 검색) | `src/search/` |
| (이름) | (예: 추천) | `src/recommendation/` |
| (이름) | (예: 서빙/대시보드) | `src/serving/`, `dashboard/` |
| (이름) | (예: 평가/문서) | `src/evaluation/`, `docs/` |

---

## 9. 개발 진행 순서

| 단계 | 내용 | 브랜치 예시 |
|---|---|---|
| 1 | 고객 행동 시뮬레이터 | `feat/simulator` |
| 2 | CLIP + FAISS 검색 API | `feat/search-api` |
| 3 | Two Tower 후보 생성 | `feat/two-tower` |
| 4 | DeepFM 랭킹, 추천 API | `feat/deepfm-ranking` |
| 5 | 리랭킹, MAB, 세션 추천 | `feat/reranking-mab` |
| 6 | Feature Store, A/B 테스트, 대시보드 | `feat/feature-store` 외 |
| 7 | 재학습 파이프라인, 문서화 | `feat/ct-pipeline`, `docs/reports` |

---

## ❓ 자주 묻는 질문

**Q. `git push`가 거부돼요.**
`main`에는 직접 올릴 수 없습니다. 내 브랜치를 만들어 올린 뒤 PR을 만드세요.

**Q. 커밋 메시지를 잘못 썼어요.**
아직 푸시 전이라면 `git commit --amend`로 마지막 메시지를 고칠 수 있습니다.

**Q. PR에서 충돌(conflict)이 났어요.**
`git fetch origin` → `git merge origin/main`으로 받아 와서 충돌 부분을 고친 뒤 다시 푸시하세요.

**Q. `docker compose`가 "no configuration file provided"라고 해요.**
`docker-compose.yml`이 있는 프로젝트 폴더로 이동한 뒤 실행하세요.
