---
created: 2026-07-06
tags: [project]
status: active
github: https://github.com/kwsahe/k-safety-law-rag
stack: Python, ChromaDB, LangChain(경량 자체 그래프), BAAI/bge-m3, Qwen2.5-14B-Instruct(Colab Pro), EXAONE-3.5-7.8B(비교), Ollama qwen2.5:3b(로컬), FastAPI, ngrok, SQLite, Flask
---

# K-Safety Law RAG

## 개요
산업안전보건법 + 중대재해처벌법(건설현장 한정) 기반 법령 검색·판단 RAG 시스템.
건설현장 사고 시나리오를 입력하면 위반 조항, 책임 판단, 재발방지 조치, 과태료 기준까지 자동 산출하고 보고서/DB 연동용 payload를 생성한다.

## 기술 스택
- **RAG 코어**: Python, ChromaDB, BAAI/bge-m3 (1024차원 임베딩)
- **LLM**: Qwen2.5-14B-Instruct (Colab Pro, 4bit 양자화, 운영 모델) / EXAONE-3.5-7.8B-Instruct (비교·백업) / qwen2.5:3b (Ollama 로컬 폴백)
- **LLM 서빙**: FastAPI (OpenAI 호환 `/v1/chat/completions`) + ngrok 터널
- **라우팅**: 경량 자체 구현 그래프 모듈(`rag/question_graph.py`) — 추후 LangGraph 전환 고려
- **웹/DB**: Flask, SQLite (users/sessions/scenarios/conversations/messages/deletion_logs)
- **표 처리**: pdfplumber 기반 표 추출·청킹 전용 모듈 (`rag.table_*`)

## 주요 기능
- **Text RAG + Table RAG 이중 구조**: 법령 조문(텍스트)과 별표/표를 별도 ChromaDB 컬렉션(`korean_safety_laws`, `law_tables`)으로 분리 검색
- **사고 시나리오 기반 위반 판단**: 굴착·크레인·비계 등 사고 시나리오 입력 → 위반 여부(YES/NO), 위반 조항, 책임 판단 자동 생성
- **질문 유형별 결정형(deterministic) 답변 분기**: 굴착 특별교육, 과태료(별표35), 표지 책임, 재발방지 조치 등은 LLM 환각을 피하기 위해 검색 근거 기반 직접 답변 경로 사용
- **QuestionScopeNode 라우팅**: 단순 법령 질문(`general_law`)과 시나리오 판단 질문(`scenario_judgment`)을 분리 처리
- **Colab Pro 원격 LLM 서빙**: 로컬은 RAG 검색만 담당, LLM 추론은 Colab GPU + ngrok으로 분리
- **보고서 payload 생성**: `reports.why_items`, `reports.compliance_levels`, `reports.final_opinion`, `reports.overall_risk_score` 구조로 보고서/DB 파트에 전달
- **ChatGPT형 웹 챗봇 UI**: 좌측 사이드바 + 시나리오 모드/일반 모드 분리, 관리자(CLI·근거·응답시간 노출)/일반 계정(답변만 노출) 권한 분리

## 진행 상황
- [x] Text RAG 파이프라인 구축 (ingest / embedder / retriever / chatbot)
- [x] Table RAG 통합 (표 추출·청킹·검색·보고서, 스모크 테스트 15/15 통과)
- [x] 산업안전보건법 건설현장 한정 데이터 전환 및 전체 재임베딩 (335청크)
- [x] Colab Pro 원격 LLM 연동, EXAONE 7.8B vs Qwen2.5-14B 비교 후 Qwen 채택
- [x] Q1~Q5 사고 판단 시나리오 결정형 답변 경로 안정화
- [x] 사고 시나리오 정본화 (`scenarios/default_accident.py`) + DB_PAYLOAD 분리
- [x] 보고서/DB 연동용 payload 스키마 정렬 (`reports.*`)
- [x] 웹 챗봇 UI ChatGPT형 레이아웃 재작성, 계정별 권한 분리
- [x] GitHub 최초 공개 (2026-06-12, Initial commit 123 files)
- [ ] LangGraph 기반 라우팅 고도화 (IntentClassifierNode, CitationValidatorNode, CacheGuardNode)
- [ ] 보고서 PDF 렌더링 파이프라인 연결
- [ ] `reports.compliance_levels` / `overall_risk_score` DB 컬럼명 최종 확정

## 개발 타임라인
| 날짜 | 주요 내용 |
|------|-----------|
| 2026-05-23 | Claude Code로 작업 이전. ingest/retriever/chatbot/law_mapper 초기 구현 |
| 2026-05-25 | law_mapper 완성. Qwen thinking 모드로 인한 570초 응답·빈 답변 버그 발견 |
| 2026-05-26 | 근본 원인 파악 후 non-thinking 모델(qwen2.5:3b)로 교체, CPU/GPU 버전 분리, 스트리밍 응답 전환 |
| 2026-05-28 | 텍스트 RAG와 표 RAG(`rag_table`)를 `rag` 패키지로 통합, 스모크 테스트 15/15 |
| 2026-05-29 | 표 추출 헤더 오인식 버그 수정, 청킹 전략 추가, 시행규칙 우선 랭킹 보정, 사고 시나리오 컨텍스트 기능 추가 |
| 2026-05-31 | 산안법 데이터 건설현장 한정 버전으로 교체, 청킹 최적화, 전체 재임베딩(335청크), Q1~Q5 테스트 |
| 2026-06-02 | Colab 원격 LLM 연동, EXAONE 7.8B vs Qwen2.5-14B 비교 → Qwen 채택, Q1/Q4/Q5 결정형 답변 도입 |
| 2026-06-03 | Gemini 평가 결과 반영, Q3/Q4/Q5 근거 정제, 참고근거 노출량 23개→7개로 축소 |
| 2026-06-10 | 사고 시나리오 정본화, DB_PAYLOAD 분리, report_scenario_runner 개선 |
| 2026-06-12 | 보고서 payload 변수명(`reports.*`) 정렬, 12페이지 이행수준 산출 추가, ngrok/방화벽 오류 처리 개선 → **GitHub 최초 공개** |
| 2026-06-13 | 웹 챗봇 UI 파스텔 블루 톤 재구성, 채팅 관리(이름수정/삭제) 기능, 비계 특별교육 라우팅 개선 |
| 2026-06-15 | ChatGPT형 레이아웃 전체 재작성, QuestionScopeNode/LangGraph 기반 라우팅 도입, 계정별 DB 구조 확정 |

## 이슈 & 해결
| 날짜 | 이슈 | 해결 |
|------|------|------|
| 2026-05-23 | "제32조의2" 형태 조항 번호 정규식 매칭 실패 | 가지번호 선택적 매칭 정규식으로 수정. [[error-2026-05-23-article-number-regex]] |
| 2026-05-25 | Qwen3.5 thinking 모드로 응답 570초·빈 답변 발생 | `ollama.generate()`→`ollama.chat()` 전환, 최종적으로 non-thinking 모델(qwen2.5:3b) 교체로 근본 해결. [[error-2026-05-25-ollama-thinking-mode]] |
| 2026-05-29 | 표 추출 시 헤더 없는 표의 첫 데이터 행이 컬럼명으로 오인식 | 항목 번호 패턴(`^\d+\.`) + 컬럼 수 조건으로 헤더 유무 판별. [[error-2026-05-29-table-header-bug]] |
| 2026-05-29 | 병합 셀 처리 누락으로 서로 다른 항목 내용이 검색 결과에 혼입 | 항목 번호 기준 `chunk_by_item()` 전략 추가. [[error-2026-05-29-table-chunk-item-mixing]] |
| 2026-05-29 | 시행령이 시행규칙보다 코사인 유사도 높게 나와 랭킹 역전 | 시행규칙 문서 score에 +0.07 보정 후 재정렬. [[error-2026-05-29-ranking-inversion]] |
| 2026-05-31 | `keep_separator` 미설정으로 "제X조" 조문 번호 패턴 소실 | `keep_separator=True`로 조항 번호 보존. [[error-2026-05-31-keep-separator]] |
| 2026-05-31 | PowerShell + 한글 경로에서 cp949 UnicodeEncodeError | `PYTHONIOENCODING=utf-8` 및 Git Bash 실행으로 우회. [[error-2026-05-31-cp949-encoding]] |
| 2026-06-02 | 굴착 질문에 무관한 시나리오 단서(크레인 등)까지 확장되어 답변 혼입 | 굴착 중심 질문은 결정형 답변 경로로 분리, 관련 근거만 우선 정렬. [[error-2026-06-02-query-scope-overreach]] |
| 2026-06-02 | Qwen 3B 모델이 검색 결과 무시하고 조항 번호 환각 | Qwen2.5-14B(Colab)로 교체 + 질문 유형별 결정형 답변 경로 도입 |
| 2026-06-02 | 긴 컨텍스트에서 LLM이 프롬프트/검색 원문을 그대로 출력 | 필요한 근거만 강제 포함해 컨텍스트 축소, 결정형 답변으로 우회. [[error-2026-06-02-long-context-prompt-leak]] |
| 2026-06-03 | 별표 supplement가 원본 청크 메타데이터를 물려받아 조항 번호 혼동 | `article`/`annex`/`violation_article` 필드 분리. [[error-2026-06-03-metadata-field-bleed]] |
| 2026-06-03 | 외부 평가자가 페이지 번호를 환각으로 오판(원문 vs 발췌본 기준 차이) | 코드 버그 아님으로 판단, 페이지 표기 방식 통일 과제로 이관. [[error-2026-06-03-page-basis-mismatch]] |
| 2026-06-03 | 결정형 답변 사용 시에도 참고근거에 미사용 근거 23개까지 노출 | `direct_answer_sources()`로 실제 사용 근거만 반환(7개로 축소) |
| 2026-06-12 | Colab/ngrok 연결 실패 시 원인 불명 상태로 조용히 종료 | 상세 오류 메시지(WinError 10013, 방화벽/ngrok 헤더 안내) 출력 개선. [[error-2026-06-12-ngrok-connection]] |
| 2026-06-12 | bge-m3 로딩 시 HuggingFace 재확인 요청으로 멈춘 것처럼 보임 | `local_files_only=True`로 네트워크 확인 생략. [[error-2026-06-12-huggingface-hang]] |
| 2026-06-13 | 새 상담 생성 API에서 `ts` 변수 미정의 | 상담 생성 시점에 `ts` 명시적 초기화. [[error-2026-06-13-chat-ts-undefined]] |

## 참고 자료
- GitHub: https://github.com/kwsahe/k-safety-law-rag
- 개발일지 원본: `C:\rag_report\devlog\`
- Colab 노트북: `qwen25_14b_colab_pro_server.ipynb`, `exaone_colab_pro_server.ipynb`
- 관련 에러 로그: `03-projects/k-safety-law-rag/errors/` (14건, 위 "이슈 & 해결" 표에서 링크 참조)
