---
created: 2026-07-06
tags: [project]
status: active
github: https://github.com/kwsahe/construction-accident-vl-agent
stack: React, Vite, TypeScript, FastAPI, OpenCV, Qwen2.5-VL/Qwen3-VL(Colab), YOLO(pretrained), pandas/matplotlib/seaborn
---

# Construction Accident VL Agent

## 개요
건설현장 CCTV 사고 영상을 업로드(또는 YouTube URL 입력)하면 사고 유형·부상자 수·사고 원인을 Vision-Language 모델이 구조화해서 판단하는 사고 분석 Agent.

> 이전 명칭은 "SPilot"이었으나, 법령 위반 판단(=K-Safety Law RAG의 역할) 중심에서 **영상 기반 사고 원인 분석** 중심으로 방향을 전환하며 2026-06-21에 SPilot 브랜딩을 제거했다. 법령 RAG와의 직접 연동은 현재 범위에서 제외되어 있다 (로드맵 항목으로 남아있음).

## 기술 스택
- **Frontend**: React + Vite + TypeScript
- **Backend**: FastAPI
- **VL 추론 서버**: Colab + Qwen2.5-VL-32B-Instruct (1순위) / Qwen2.5-VL-7B-Instruct (VRAM 부족 시 fallback) → Qwen3-VL-32B로 전환 예정
- **비교 모델**: InternVL3, LLaVA-OneVision-2-8B, MiniCPM-V 4.5 (평가용 Colab 서버 노트북 보유)
- **영상 처리**: OpenCV (프레임 추출 → contact sheet 생성)
- **보조 탐지**: YOLO pretrained `.pt` adapter (커스텀 학습 없이 inference만 수행하는 보조 evidence)
- **평가 시각화**: pandas, matplotlib, seaborn

## 핵심 아이디어
원본 mp4 전체를 모델에 그대로 넣지 않고, 로컬 Agent가 의미 있는 프레임만 추출해 한 장의 **contact sheet** 이미지로 압축한다. VL 모델은 이 contact sheet를 보고 사고 전후 시간순 변화(작업자 위치, 구조물 이동)를 비교해 원인을 추론한다.

```text
mp4 업로드/YouTube URL -> video 폴더 저장 -> 프레임 추출 -> contact sheet 생성
-> (선택) YOLO pretrained 보조 evidence -> Qwen VL 사고 분석
-> 사고 유형/부상자 수/원인 JSON -> 분석 payload 변환 -> 프론트엔드 시각화
```

## 주요 기능
- **영상 업로드 및 재사용**: mp4/mov/avi/mkv 업로드 → `video/` 폴더 저장, 저장된 영상 목록에서 재분석 가능
- **사고 순간 자동 탐지**(`--auto-moment`): overview contact sheet로 먼저 사고 발생 구간을 추정
- **사고 유형·원인 판단**: `primary_type`(낙상/추락/화재/기타), `injured_count`, `cause`, `timeline`, `evidence`를 JSON으로 생성 — 법적 책임/과실은 단정하지 않고 영상에서 관찰 가능한 사실만 근거로 사용
- **분석 payload 변환**: Qwen 응답을 바로 DB에 넣지 않고 `agent/save_judgment.py`에서 `judgment.*`, `video_part_tables.cctv_events[]`, `evidence_photos[]` 구조로 변환
- **평가 대시보드**: Qwen2.5-VL, Qwen3-VL, InternVL3, LLaVA-OneVision, MiniCPM-V 등 모델/프롬프트별 정확도·latency 비교 (accident type accuracy, cause keyword recall, JSON valid rate 등)

## 진행 상황 (README STEP/Phase 기준)
- [x] React+Vite+TS 프론트엔드, FastAPI 백엔드, Colab Qwen2.5-VL 서버 연동 (v1)
- [x] Contact sheet 기반 사고 전후 비교 파이프라인 구축
- [x] SPilot 브랜딩 제거, 사고 원인 판단 중심으로 리포지셔닝 (2026-06-21)
- [x] YOLO pretrained 보조 evidence 워크플로우 추가
- [x] 로컬 Ollama 연동 + YOLO 미리보기 워크플로우
- [x] 평가 대시보드 및 모델 서버 노트북(Qwen2.5-VL/Qwen3-VL/InternVL3/LLaVA/MiniCPM) 추가
- [x] 평가 DB 및 filtered YOLO evidence 워크플로우
- [ ] Qwen3-VL-32B를 주 reasoning 모델로 전환
- [ ] YouTube URL 입력 지원 (`yt-dlp` 연동)
- [ ] 사고보고서 초안(`report_draft`) 및 재발 방지 조치(`prevention_actions`) 생성
- [ ] 평가 자동화(`eval/run_evaluation.py`) 및 시각화 차트 프론트엔드 탑재
- [ ] 법령 RAG(K-Safety Law RAG) 연동 — 로드맵 최종 단계

## 개발 타임라인 (GitHub 커밋 기준)
| 날짜 | 내용 |
|------|------|
| 2026-06-21 | 최초 커밋 (Initial construction accident VL agent) |
| 2026-06-21 | 사고 원인 판단 중심으로 리포지셔닝, SPilot 브랜딩 제거 |
| 2026-06-28 | 평가 대시보드 및 모델 서버 노트북(Qwen2.5-VL/Qwen3-VL/InternVL3/LLaVA-OneVision/MiniCPM-V) 추가 |
| 2026-06-29 | 로컬 Ollama 연동 + YOLO 미리보기 워크플로우 추가 |
| 2026-06-29 | 평가 DB 및 filtered YOLO evidence 워크플로우 추가 |

## 이슈 & 해결
| 날짜 | 이슈 | 해결 |
|------|------|------|
|  | (로컬 devlog 미보유 — 저장소 커밋 메시지 기준으로만 정리됨) |  |

## 참고 자료
- GitHub: https://github.com/kwsahe/construction-accident-vl-agent
- 관련 문서: `docs/PORTFOLIO.md`(포트폴리오 서술), `docs/ROADMAP.md`(Phase 1~6 상세 계획), `docs/STRUCTURE.md`(폴더 구조)
- 관련 프로젝트: [[k-safety-law-rag/README|K-Safety Law RAG]] — 법령 RAG 연동은 로드맵상 향후 과제
