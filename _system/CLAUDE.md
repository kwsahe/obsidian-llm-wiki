# CLAUDE.md — kwsahe's AI Second Brain

> 이 파일은 Claude Code가 매 세션 시작 시 자동으로 읽는 컨텍스트 파일입니다.
> 새 대화를 시작할 때마다 여기 적힌 내용을 기반으로 나를 파악하고 작업하세요.

---

## 👤 나에 대해

- **이름**: 권상헌 (kwsahe)
- **학력**: 서강대학교 미디어공학과 졸업
- **현재 상태**: 데이터 엔지니어 / AI 개발자 취업 준비 중
- **목표 직무**: 데이터 엔지니어, AI 개발자 (RAG·LLM·컴퓨터비전 관련)
- **주요 언어**: Python (메인), 영어/한국어 혼용 작업 환경
- **개발 환경**: Windows + Git Bash, conda 가상환경, VS Code, Claude Code

---

## 🚀 포트폴리오 프로젝트

### 1. K-Safety Law RAG
- **GitHub**: https://github.com/kwsahe/k-safety-law-rag
- **설명**: 산업안전보건법 + 중대재해처벌법 기반 법령 검색·판단 RAG 시스템
- **스택**: Python, ChromaDB, LangChain, BAAI/bge-m3, Qwen2.5-14B (Colab Pro), SQLite, Flask
- **특징**: Text RAG + Table RAG 분리, 별표/표 전용 컬렉션, CLI + 웹앱(web_app.py), 사용자별 대화 이력, admin/일반 계정 분리
- **현재 이슈**: `localhost/admin/agent` 라우팅 로직 → 고정 Qwen 판단값으로 교체 예정

### 2. SPilot (건설현장 VL 에이전트)
- **설명**: 건설현장 사고 시나리오 → 산안법/중처법 위반 여부 자동 판단 시스템
- **스택**: Python, Qwen2.5-14B, LangChain, ChromaDB, JSON 구조화 출력
- **출력 구조**: 위반 조항, 책임 판단, 최종 평가 → DB 삽입
- **상태**: v1 안정화 완료. LangGraph ReAct Agent는 v2로 연기

### 3. O2O 수요 예측 서비스
- **설명**: 배달/방문 수요 예측 모델을 Flask API로 서비스화
- **스택**: Python, Flask, Naver Maps API
- **특징**: 공개 API, AI 챗봇, 지도 연동

### 4. Artesia (로그라이크 게임)
- **설명**: Unity 2D 기반 로그라이크 RPG (솔로 리빌드 계획 중)
- **스택**: Unity, C#
- **AI 파이프라인 계획**: Stable Diffusion + ComfyUI + ControlNet으로 애셋 자동 생성

---

## 🛠 기술 스택

| 분야 | 기술 |
|------|------|
| LLM/RAG | LangChain, LangGraph, ChromaDB, Ollama, Qwen2.5, EXAONE |
| 임베딩 | BAAI/bge-m3 |
| 백엔드 | Flask, Django REST Framework |
| DB | SQLite, MariaDB, ChromaDB |
| 컴퓨터비전 | YOLO, ByteTracker (학습 중) |
| AI 이미지 생성 | Stable Diffusion, ComfyUI, ControlNet |
| 인프라/도구 | Git, GitHub, conda, VS Code, Claude Code |

---

## 🎯 취업 준비 현황

- **목표 직무**: 데이터 엔지니어, AI 개발자
- **최근 전형**: 인턴십 프로그램 (~24개 기업) 서류/면접 진행
  - 면접 경험 기업: 디엠티랩스, 에스에이치엘에이비, 유니에스아이엔씨, 스칼라웍스, 클레버러스
- **관심 기업 유형**: RAG·AI 솔루션, 건설/안전 AI, O2O/물류 플랫폼
- **포폴 링크**: https://kwsahe.github.io/kwsahe

---

## 🎮 관심사 & 사이드 프로젝트

- **게임**: 원신 (GIMI/XXMI 모드 작업 중), 붕괴: 스타레일, 심즈 4
- **AI 이미지**: Stable Diffusion, ComfyUI, 애니 스타일 생성 (Danbooru 태그 기반)
- **YOLO + ByteTracker 프로젝트**: 개인 포폴용 기획 중 (주제 미확정)

---

## 📁 Vault 구조

```
kwsahe-brain/
├── 00-inbox/          ← 미분류 임시 보관 (일단 여기 던지기)
├── 01-atlas/          ← 기술 개념 위키 (LLM, RAG, CV 등)
├── 02-calendar/       ← 일일/주간 기록
├── 03-projects/       ← 프로젝트별 노트
│   ├── k-safety-law-rag/
│   ├── construction-vl-agent/
│   ├── o2o-forecasting/
│   ├── artesia/
│   └── job-search/
├── 04-resources/      ← 강의 노트, 참고자료, 링크
├── 05-archive/        ← 완료 보관
├── 06-ideas/          ← 프로젝트 영감/아이디어 노트
└── _system/           ← 템플릿, 이 CLAUDE.md
    ├── CLAUDE.md      ← 지금 이 파일
    └── templates/     ← daily-note / project-note / error-log / interview-qa / idea-note / claude-tool-note
```

---

## 📌 Claude Code 작업 규칙

1. **노트 생성 시** → 항상 frontmatter(YAML) 포함
   ```yaml
   ---
   created: YYYY-MM-DD
   tags: []
   project: 
   status: draft | active | done
   ---
   ```
2. **파일 저장 위치** → 애매하면 `00-inbox/`에 저장 후 나에게 확인 요청
3. **기존 노트 수정 시** → 수정 전 내용 요약을 먼저 보여주고 승인 받기
4. **검색 요청** → 키워드로 vault 전체 검색 후 관련 노트 목록 제시
5. **언어** → 한국어로 대화, 코드/명령어는 영어 유지

---

## 🔁 자주 쓰는 요청 패턴

- `"오늘 일지 만들어줘"` → `02-calendar/YYYY-MM-DD.md` 생성 (템플릿 적용)
- `"[프로젝트명] 진행 상황 정리해줘"` → 해당 프로젝트 폴더 노트 요약
- `"[키워드] 관련 노트 찾아줘"` → vault 검색 후 목록 반환
- `"에러 기록해줘"` → `03-projects/[관련프로젝트]/errors.md`에 날짜별 추가
- `"면접 질문 정리해줘"` → `03-projects/job-search/interview-qa.md`에 추가
