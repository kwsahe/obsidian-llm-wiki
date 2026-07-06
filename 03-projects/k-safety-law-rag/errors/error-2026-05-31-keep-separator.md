---
created: 2026-05-31
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: keep_separator 미설정으로 "제X조" 조항 번호 패턴 소실

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-05-31
- 스택: LangChain TextSplitter, `rag/ingest.py`

## 에러 메시지
```
(런타임 에러 아님 — 메타데이터 추출 실패로 이어짐)
extract_article_number()의 "제\d+조" 정규식이 매칭되지 않는 청크 다수 발생
```

## 원인
텍스트를 `"\n제"` 기준으로 분리할 때 `keep_separator`를 설정하지 않으면(기본값 `False`) 분리 기준이 된 `제` 글자 자체가 청크 시작 부분에서 소실된다. 그 결과 `제32조` 같은 패턴이 `32조`로 잘려 `extract_article_number()`의 `제\d+조` 정규식이 매칭에 실패하는 연쇄 버그가 발생했다.

## 해결 방법
```python
# rag/ingest.py
# 변경 전: keep_separator 미설정 (기본 False) → "제" 소실
# 변경 후:
splitter = RecursiveCharacterTextSplitter(
    separators=["\n제", ...],
    keep_separator=True,  # 분리 기준 문자를 다음 청크 시작에 유지
)
```

같은 세션에서 `law_name` 메타데이터도 파일명 stem 대신 `_metadata.json`의 정식 법령명을 조회하도록, 청크 ID도 `chunk_0` 인덱스 대신 `md5(source::page::index)` 해시로 바꿔 안정성을 함께 개선했다.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260531.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
