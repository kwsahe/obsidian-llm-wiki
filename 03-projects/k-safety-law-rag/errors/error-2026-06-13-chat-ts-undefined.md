---
created: 2026-06-13
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: 새 상담 생성 API에서 `ts` 변수 미정의

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-06-13
- 스택: `web_app.py` (Flask), 새 상담 생성 API

## 에러 메시지
```
NameError 계열 — ts 변수가 정의되지 않은 상태로 참조됨
```

## 원인
새 상담(채팅) 생성 API 핸들러에서 타임스탬프 변수 `ts`를 응답이나 DB 저장에 사용하면서 정작 함수 내에서 초기화하는 코드가 누락되어 있었다. 채팅 관리 UI(이름 수정, 삭제, soft delete 등) 기능을 추가하는 과정에서 API 응답 스키마가 확장되며 드러난 문제였다.

## 해결 방법
새 상담 생성 시점에 `ts`를 명시적으로 생성해 응답/저장 경로 모두에 일관되게 사용하도록 수정.
```python
# web_app.py
ts = datetime.now().isoformat()
# ... 응답 및 DB insert에 ts 사용
```

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260613-15.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
