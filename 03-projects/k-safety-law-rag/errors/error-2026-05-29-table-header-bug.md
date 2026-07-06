---
created: 2026-05-29
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: 표 추출 시 헤더 없는 표의 첫 데이터 행이 컬럼명으로 오인식

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-05-29
- 스택: pdfplumber, `rag/table_extraction.py`

## 에러 메시지
```
(런타임 에러 아님 — 데이터 정합성 버그)
산업안전보건법 시행규칙 별표 5 특별교육 표(p.82)에서
17번 항목이 컬럼 헤더로 처리되어 사라지고
18~22번 항목만 데이터 행으로 남는 현상 발생
```

## 원인
`raw_table_to_df()` 함수가 항상 표의 첫 번째 행을 컬럼 헤더로 취급했다.
그런데 특별교육 표(별표 5)는 헤더 행 없이 곧바로 데이터 행(17번 항목)으로 시작하는 구조라, 17번 항목 내용이 통째로 헤더 이름이 되어버리고 실제 데이터에서 누락되는 문제였다.

## 해결 방법
```python
# rag/table_extraction.py
# 첫 번째 셀이 "숫자." 패턴이고 컬럼 수가 3개 이하이면
# 헤더 없는 표로 판단해 첫 행도 데이터로 포함
if re.match(r"^\d+\.", first_cell) and num_cols <= 3:
    header = [f"col_{idx}" for idx in range(num_cols)]
    body = normalized_rows  # 첫 행도 데이터로 유지
```

컬럼 수 조건(`<= 3`)을 둔 이유: 별표 19 노출기준 표(TWA_ppm 등 5~6개 컬럼)는 정상적인 헤더 구조이므로 기존 방식을 그대로 유지해야 했기 때문. 컬럼 수로 두 표 유형을 구분해서 분기 처리했다.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260529.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
