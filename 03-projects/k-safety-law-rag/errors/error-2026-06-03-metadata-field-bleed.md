---
created: 2026-06-03
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: 별표 supplement가 원본 텍스트 청크의 메타데이터를 그대로 물려받아 조항 번호 혼동

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-06-03
- 스택: `rag/integrated_retriever.py` (Q4 과태료 답변 경로)

## 에러 메시지
```
(런타임 에러 아님 — 출처 표기 오류)
Gemini 평가에서 지적: 참고근거에 "산업안전보건법 시행령 제29조 p.130~143"처럼
법 조항과 별표 페이지가 뒤섞인 표기가 나타남
```

## 원인
별표35(과태료 기준) exact supplement를 강제로 추가할 때, 실제 텍스트 청크가 이미 갖고 있던 기존 메타데이터(`article=제29조`)를 그대로 재사용했다. 그 결과 "별표 35"라는 출처와 "제29조"라는 조항 번호가 하나의 근거 안에 섞여 출력되어, 실제로는 서로 다른 두 정보(위반 유형의 근거 조항 vs 과태료 기준표의 위치)가 마치 하나인 것처럼 보였다.

## 해결 방법
```python
# rag/integrated_retriever.py
# 별표35 supplement의 metadata를 완전히 분리
metadata = {
    "article": "",                       # 조항 필드는 비움
    "annex": "별표 35",                   # 출처는 별표 번호로 명시
    "citation_page": "130~143",
    "violation_article": "법 제29조제3항", # 위반 조항은 별도 필드로 분리
}
```

이후 출력은 "근거: 별표 35, p.130~143"과 "위반 유형: 법 제29조제3항 위반"으로 명확히 분리 표시된다.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260603.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
