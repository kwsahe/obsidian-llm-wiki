---
created: 2026-06-02
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: 굴착 관련 질문에 무관한 시나리오 단서까지 확장되어 답변 혼입

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-06-02
- 스택: Qwen2.5-14B-Instruct(Colab), `rag/chatbot.py`, `rag/integrated_retriever.py`

## 에러 메시지
```
(런타임 에러 아님 — 답변 범위 오류)
Q1 질문 의도: "굴착 작업 관련 특별안전교육 미실시를 중심으로 판단"
실제 출력: 시나리오에 포함된 "15층", "골조", "크레인" 단서까지 확장 인용
→ 별표 5 제27호, 제14호, 제39호 교육내용이 굴착(제19호) 답변에 혼입
```

## 원인
사고 시나리오 텍스트에는 굴착 외에도 여러 위험 요소(고층, 골조, 크레인)가 함께 서술되어 있는데, LLM이 질문의 초점(굴착)을 벗어나 시나리오 전체 맥락으로 답변 범위를 확장해버렸다. RAG 검색 자체는 정상이었지만, LLM이 검색 결과 중 관련 없는 근거까지 답변에 섞어 넣은 것이 문제였다.

## 해결 방법
```python
# rag/chatbot.py
# should_direct_focused_excavation_violation() 추가
# 질문이 굴착 작업 중심이면 LLM으로 보내지 않고
# direct_excavation_special_education_answer()로 별표 5 제19호만 결정형 출력

# rag/integrated_retriever.py
# _is_focused_excavation_query() 추가
# 굴착 중심 질문에서 제19호를 우선 정렬하고
# 제27호·제39호·타워크레인 근거는 감점 처리
```

질문의 초점이 명확한 유형(굴착, 표지 책임, 과태료, 재발방지 등)은 LLM의 자유 생성에 맡기지 않고 결정형(deterministic) 경로로 분기하는 것이 이 프로젝트 전반의 해결 패턴이 됐다.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260602.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
