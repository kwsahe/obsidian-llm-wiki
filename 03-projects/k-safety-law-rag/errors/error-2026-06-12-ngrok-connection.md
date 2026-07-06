---
created: 2026-06-12
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: Colab/ngrok 연결 실패 시 원인 불명 상태로 조용히 종료

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-06-12
- 스택: Windows, Colab Pro, FastAPI, ngrok, `report_scenario_runner.py`

## 에러 메시지
```
WinError 10013
액세스 권한에 의해 숨겨진 소켓에 액세스를 시도했습니다

ERR_NGROK_6024  (ngrok 무료 도메인 브라우저 경고 페이지)
```

## 원인
`report_scenario_runner.py`에서 시나리오를 선택하면 화면상 아무 반응 없이 바로 종료되는 것처럼 보였다.
원인은 두 가지:

1. RAG 검색 후 Colab/ngrok으로 LLM을 호출하는 단계에서 실패했지만, `rag_chat()` 호출 중 stdout이 숨겨져 있어 실패 원인이 터미널에 전혀 출력되지 않았음.
2. 실제 네트워크 오류는 `WinError 10013`(Windows 방화벽/백신/네트워크 정책이 ngrok HTTPS 접속을 차단)이었고, 이는 코드 버그가 아니라 로컬 환경 문제였음.
3. 별개로, ngrok 무료 도메인을 브라우저/API로 직접 호출하면 `ERR_NGROK_6024` 경고 페이지가 응답으로 오는 경우가 있는데, 이 경우 API 요청에 특정 헤더가 없으면 정상 응답 대신 경고 페이지 HTML을 받게 된다.

## 해결 방법
```python
# 1) stdout 숨김 제거 + 실패 시 상세 진단 메시지 출력
#    - RAG 검색 후 LLM 호출 실패 여부
#    - 오류 내용 (WinError 코드 등)
#    - Colab 런타임 확인 여부
#    - ngrok 터널 상태 확인 여부
#    - .env의 LLM_API_BASE 값 확인
#    - 방화벽/백신/ngrok HTTPS 차단 가능성 안내
```
```http
# 2) ngrok 무료 경고 페이지 우회 헤더 (rag/chatbot.py 원격 호출에 이미 포함)
ngrok-skip-browser-warning: true
```
```powershell
# 3) 연결 상태를 미리 점검하는 스모크 테스트 명령
Invoke-RestMethod `
  -Uri "https://YOUR_NGROK_URL/v1/models" `
  -Headers @{"ngrok-skip-browser-warning"="true"}
```

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260612.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
