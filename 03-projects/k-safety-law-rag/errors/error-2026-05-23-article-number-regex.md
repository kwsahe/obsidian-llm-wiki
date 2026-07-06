---
created: 2026-05-23
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: "제32조의2" 형태의 조항 번호 정규식 매칭 실패

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-05-23
- 스택: Python `re`, `rag/ingest.py` `extract_article_number()`

## 에러 메시지
```
(런타임 에러 아님 — 조항 번호 추출 누락)
"제32조의2" 처럼 가지번호가 붙은 조항이 메타데이터에 조항 번호로 인식되지 않음
```

## 원인
`extract_article_number()`의 정규식이 `제 N 조` 형태만 매칭하도록 작성되어 있어, 가지번호(`의2`, `의3` 등)가 붙은 조항을 처리하지 못했다.

```python
# 변경 전
re.search(r"제\s*\d+\s*조", text)
```

## 해결 방법
```python
# 변경 후 — "의 N" 부분을 선택적으로 매칭
re.search(r"제\s*\d+\s*조(?:의\s*\d+)?", text)
```

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260523.txt`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
