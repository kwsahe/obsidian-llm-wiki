---
created: 2026-05-25
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: Ollama thinking 모드로 인한 570초 응답 지연 및 빈 답변

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-05-25 ~ 2026-05-26
- 스택: Ollama 0.24.0, ollama Python 라이브러리 0.6.1, qwen3.5:4b, RTX 3050 Laptop (VRAM 4096MiB)

## 에러 메시지
```
[답변] (빈 문자열)
참고 법령: 법령명/조항 모두 빈 문자열
응답 시간: 570,630ms (약 9.5분)
```

## 원인
세 가지 문제가 겹쳐 있었다.

1. **빈 답변**: qwen3.5:4b가 thinking 모드로 `<think>...</think>` 블록을 수백 초간 생성한 뒤에야 실제 답변을 출력. `think=False` 파라미터가 실제로는 적용되지 않고 있었음.
2. **빈 법령명**: 이전 버전 코드로 임베딩된 데이터에 `law_name` 필드가 아예 없었음 (재임베딩 전 상태).
3. **570초 지연의 근본 원인**: RTX 3050 VRAM 4096MiB 한도에서 qwen3.5:4b(3.4GB) + 기본 컨텍스트(32768토큰) KV캐시(~760MiB)를 합치면 4,160MiB로 VRAM을 초과 → 모델이 CPU/GPU로 분할 실행되며 극도로 느려짐.

추가 디버깅 과정에서 밝혀진 사실:
- `ollama.generate()`는 raw prompt를 그대로 전달해 Qwen3 계열의 모델 템플릿을 건너뛰기 때문에, 프롬프트에 `/no_think`를 넣어도 실제로 인식되지 않음.
- `think=False`를 `ollama.chat()`에 직접 전달하면 Ollama 0.24.0 서버가 응답 자체를 멈추는(hang) 문제 발생.
- Modelfile에 `PARAMETER think false`를 넣어도 Ollama 0.24.0은 `unknown parameter 'think'` 오류로 미지원.

## 해결 방법
```python
# 1) num_ctx 축소로 VRAM 여유 확보
options = {"temperature": 0.3, "num_ctx": 8192}  # KV캐시 ~190MB로 축소

# 2) generate() -> chat()으로 전환 (모델 템플릿이 적용되어야 /no_think가 실제로 동작)
ollama.chat(model, messages=[
    {"role": "system", "content": "...규칙...\n/no_think"},
    {"role": "user", "content": question},
], options=options)

# 3) think=False 파라미터는 서버 hang을 유발하므로 제거하고
#    <think> 블록 정규식 제거를 fallback으로 유지

# 4) 근본 해결: non-thinking 모델로 교체
# config.py
LLM_MODEL = "qwen2.5:3b"  # 2GB, thinking 없음, 한국어 우수, VRAM에 완전 탑재 가능
```

재임베딩(`python scripts/run_ingest.py --reset`)으로 `law_name` 필드 누락 문제도 함께 해결.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260525.txt`, `devlog_260526.txt`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
