---
created: 2026-06-12
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: bge-m3 임베딩 모델 로딩 시 HuggingFace 재확인 요청으로 멈춘 것처럼 보임

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-06-12
- 스택: `sentence-transformers`, `rag/embedder.py`, BAAI/bge-m3

## 에러 메시지
```
(런타임 에러 아님 — 응답 없음처럼 보이는 지연)
로컬에 모델이 이미 캐시되어 있는데도 실행할 때마다 응답이 없는 것처럼 멈춤
```

## 원인
`SentenceTransformer("BAAI/bge-m3")`를 기본 옵션으로 호출하면 로컬 캐시가 있어도 HuggingFace Hub에 최신 버전 여부를 확인하는 HEAD 요청을 매번 보낸다. 네트워크 상태가 느리거나 불안정하면 이 요청이 재시도되며 화면상 아무 출력 없이 멈춘 것처럼 보이는데, 실제로는 모델 로딩과 무관한 네트워크 확인 단계에서 지연되고 있었다.

## 해결 방법
```python
# rag/embedder.py
model = SentenceTransformer(
    "BAAI/bge-m3",
    local_files_only=True,  # 로컬 캐시만 사용, 네트워크 확인 생략
)
# 로컬 캐시가 없으면 명확한 오류 메시지 출력
# 로딩 로그에 flush=True 적용해 버퍼링으로 인한 출력 지연도 제거
```

주의: 모델을 한 번도 받아본 적 없는 PC에서는 최초 1회는 인터넷 연결 상태에서 다운로드가 필요하다.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260612.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
