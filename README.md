# obsidian-llm-wiki

권상헌(kwsahe)의 개인 AI 세컨드브레인 Obsidian vault. 데이터 엔지니어/AI 개발자 취업 준비와 포트폴리오 프로젝트 개발 기록을 Claude Code와 함께 정리한다.

## 구조

```
obsidian-llm-wiki/
├── 00-inbox/          미분류 임시 메모
├── 01-atlas/          Dataview 대시보드 등 전체 현황 뷰
├── 02-calendar/       일일 개발/취준 기록
├── 03-projects/       프로젝트별 노트 (아래 참고)
├── 04-resources/      강의 노트, 참고자료
├── 05-archive/        완료된 항목 보관
├── 06-ideas/          프로젝트 영감/아이디어 노트
├── docs/              개발지시서, 초기 안내 노트 (로컬 전용, git 미추적)
└── _system/           템플릿, 자동화 스크립트, CLAUDE.md
    ├── templates/     daily-note / project-note / error-log / interview-qa / idea-note / claude-tool-note
    └── scripts/       daily_note_gen.py
```

## 프로젝트 노트 ([03-projects](03-projects))

| 프로젝트 | 설명 | GitHub |
|---|---|---|
| [k-safety-law-rag](03-projects/k-safety-law-rag/README.md) | 산업안전보건법·중대재해처벌법 기반 법령 검색·판단 RAG | [kwsahe/k-safety-law-rag](https://github.com/kwsahe/k-safety-law-rag) |
| [construction-vl-agent](03-projects/construction-vl-agent/README.md) | 건설현장 CCTV 사고 영상 분석 Vision-Language Agent | [kwsahe/construction-accident-vl-agent](https://github.com/kwsahe/construction-accident-vl-agent) |
| [o2o-forecasting](03-projects/o2o-forecasting/README.md) | 실거래가 기반 인테리어 수요 예측 파이프라인 | [kwsahe/O2O-demand-forecasting-solution](https://github.com/kwsahe/O2O-demand-forecasting-solution) |
| [job-search](03-projects/job-search/README.md) | 취업 준비 활동, 지원/면접 현황 ([companies.md](03-projects/job-search/companies.md)) | - |

각 프로젝트 노트는 실제 개발일지(devlog)와 GitHub 커밋 이력을 근거로 작성되며, 재사용 가치가 높은 버그는 `errors/` 하위에 개별 기록으로 남긴다 (예: [k-safety-law-rag/errors](03-projects/k-safety-law-rag/errors)).

## 자동화

- **템플릿**: Templater 문법 기반 4종(`_system/templates/`) — 새 노트 생성 시 커맨드 팔레트에서 바로 적용
- **대시보드**: [01-atlas/dashboard.md](01-atlas/dashboard.md) — Dataview로 진행 중 프로젝트, 최근 일일 노트, 미해결 에러, 면접 기록을 자동 집계
- **일일 노트 자동 생성**: `python _system/scripts/daily_note_gen.py` — 오늘 날짜 노트를 `02-calendar/`에 생성 (이미 있으면 스킵)

## 필요 Obsidian 플러그인

- Dataview
- Templater
- Calendar
- Local REST API (선택)

## 작업 규칙

자세한 작업 규칙과 컨텍스트는 [_system/CLAUDE.md](_system/CLAUDE.md) 참고.
