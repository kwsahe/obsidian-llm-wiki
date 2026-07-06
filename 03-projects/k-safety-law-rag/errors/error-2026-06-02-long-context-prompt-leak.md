---
created: 2026-06-02
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: 긴 컨텍스트에서 LLM이 프롬프트/검색 원문을 답변으로 그대로 출력

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-06-02
- 스택: Qwen2.5-14B-Instruct(Colab), `rag/chatbot.py` (Q5 재발방지 조치 질문)

## 에러 메시지
```
(런타임 에러 아님 — 출력 형식 붕괴)
서에 따라 확인을 받아야 하는 사업주가...
[노트]
...
[질문]
사고가 발생한 후 사업주가 즉시 취해야 할 조치는?
```

## 원인
Q5(재발방지 조치)는 종합 판단 문항이라 보강 근거가 많아 검색 결과가 20개 이상 참고 근거로 포함됐다. 컨텍스트가 길어지자 Qwen2.5-14B가 "답변 지시"와 "검색된 원문/프롬프트 텍스트"의 경계를 잃고, 프롬프트에 포함된 법령 원문이나 지시문 조각을 그대로 이어서 출력해버렸다.

## 해결 방법
```python
# rag/integrated_retriever.py
# _prevention_text_supplements(), _prevention_table_supplements() 추가
# 재발방지 질문에서 필요한 근거(특별교육/출입통제/크레인 검사/재해보고 등)를
# 최소한으로 강제 포함시켜 컨텍스트 길이 자체를 줄임

# rag/chatbot.py
# PREVENTION_ACTION_PROMPT + direct_prevention_action_answer() 추가
# 재발방지 질문은 LLM에 긴 컨텍스트를 통째로 넘기지 않고
# 검색 근거 기반 결정형 조치 목록을 코드에서 직접 조립
```

근본적으로는 "컨텍스트가 길어질수록 모델이 지시-원문 경계를 잃을 위험이 커진다"는 일반적인 LLM 특성이 원인이므로, 긴 컨텍스트를 줄이거나 결정형 경로로 우회하는 것이 가장 안정적인 해결책이었다.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260602.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
