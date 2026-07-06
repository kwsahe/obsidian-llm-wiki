---
created: 2026-05-29
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: 표 청킹 시 병합 셀 처리 누락으로 서로 다른 항목 내용이 혼입

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-05-29
- 스택: pdfplumber, `rag/table_chunking.py`

## 에러 메시지
```
(런타임 에러 아님 — 벡터 검색 품질 저하)
19번·17번·22번 특별교육 항목의 교육 내용이 검색 결과에서 서로 섞여 나옴
```

## 원인
pdfplumber가 PDF의 병합 셀(rowspan)을 `None` → 빈 문자열(`""`)로 변환하는데, 연속된 여러 행이 항목 번호 없이 이어지다 보니 어느 행이 몇 번 항목에 속하는지 구분할 근거가 사라졌다. 그 결과 row 단위로 청킹하면 서로 다른 항목의 교육 내용이 하나의 벡터에 섞여 들어가는 문제가 발생했다.

## 해결 방법
```python
# rag/table_chunking.py
# "^\d+\." 패턴이 있는 행을 기준으로, 그 다음에 오는
# 번호 없는 연속 행들을 하나의 청크로 묶는 chunk_by_item() 전략 추가
def chunk_by_item(df, base_metadata):
    # [작업항목] {번호} / [교육내용] {내용} 형식으로 포맷
    ...

# 노출기준 표처럼 컬럼명이 있는 표(TWA_ppm 등)는 항목 번호 패턴이 없으므로
# chunk_by_row로 자동 폴백
EXPOSURE_COLS = {"TWA_ppm", "STEL_ppm", "TWA_mg_m3", "STEL_mg_m3", "유해인자", "허용기준"}
if EXPOSURE_COLS & set(cleaned.columns):
    return chunk_by_row(df, base_metadata)
```

부가적으로, 청킹 포맷에 `col_0: 19. 굴착면...`처럼 항목 번호가 헤더(`[작업항목]`)와 본문에 중복 출력되어 LLM이 `col_0`, `col_1` 같은 내부 컬럼명을 그대로 노출하는 문제도 함께 수정 — 첫 번째 컬럼(항목 번호)을 본문에서 제거하고 `col_X` 접두어 없이 값만 출력하도록 했다.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260529.md`
- 관련: [[error-2026-05-29-table-header-bug]]
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
