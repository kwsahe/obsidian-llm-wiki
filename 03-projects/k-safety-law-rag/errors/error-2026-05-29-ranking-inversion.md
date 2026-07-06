---
created: 2026-05-29
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: 시행령이 시행규칙보다 유사도 높게 나와 검색 랭킹 역전

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-05-29
- 스택: ChromaDB 코사인 유사도, `rag/integrated_retriever.py`

## 에러 메시지
```
(런타임 에러 아님 — 검색 랭킹 품질 문제)
시행령(추상적 규정)이 시행규칙(구체적 별표 수치 기준)보다 항상 1위로 검색됨
예: 시행령 p.47이 매번 1위, 실제 필요한 시행규칙 별표는 4위 이하로 밀림
```

## 원인
법령 조문 임베딩만으로는 "얼마나 구체적인 기준을 담고 있는가"를 반영하지 못한다. 시행령의 추상적 표현이 질문 임베딩과 코사인 거리상 더 가깝게 나오는 경우가 있어, 실제 사용자가 필요로 하는 시행규칙 별표(수치 기준)가 하위 랭킹으로 밀려나는 문제가 반복적으로 발생했다.

## 해결 방법
```python
# rag/integrated_retriever.py
_SIHAENGGYUCHIK_BONUS = 0.07

def _is_sihaenggyuchik(metadata: dict) -> bool:
    name = str(metadata.get("law_name", "") or "")
    return "시행규칙" in name

# 시행규칙 문서의 score에 +0.07 보정 후 재정렬
```

결과: 시행령 p.47 → 4위로 하락, 시행규칙 p.82 관련 항목들이 1~3위로 상승.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260529.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
