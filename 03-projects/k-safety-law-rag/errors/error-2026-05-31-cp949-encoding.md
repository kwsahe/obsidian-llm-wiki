---
created: 2026-05-31
tags: [error]
project: k-safety-law-rag
status: resolved
---

# 에러: PowerShell + 한글 경로에서 cp949 UnicodeEncodeError

## 발생 환경
- 프로젝트: K-Safety Law RAG
- 날짜: 2026-05-31
- 스택: Windows PowerShell, Python, 한글 파일 경로(`data/laws/02_산업안전보건법/...`)

## 에러 메시지
```
UnicodeEncodeError: 'cp949' codec can't encode character ... in position ...
```

## 원인
Windows PowerShell의 기본 콘솔 코드페이지가 cp949(EUC-KR 계열)라서, Python 프로세스의 표준 출력/에러 스트림이 cp949로 인코딩을 시도한다. 파일 경로나 로그 문자열에 cp949로 표현 불가능한 한글 조합이나 특수 문자가 섞여 있으면 `print()` 시점에 인코딩 에러가 발생해 재임베딩(`python scripts/run_ingest.py --reset`) 같은 장시간 작업이 중간에 죽는다.

## 해결 방법
```powershell
# 방법 1: 환경변수로 강제 UTF-8 출력 + 실행파일 직접 지정
$env:PYTHONIOENCODING = "utf-8"
python scripts/run_ingest.py --reset
```

가장 안정적인 우회는 **PowerShell 대신 Git Bash(Bash 툴)로 실행**하는 것이었다 — Git Bash는 기본적으로 UTF-8 로케일을 사용해 동일한 문제가 재현되지 않았다.

## 참고 링크
- 개발일지: `C:\rag_report\devlog\devlog_260531.md`
- [[k-safety-law-rag/README|K-Safety Law RAG 프로젝트 노트]]
