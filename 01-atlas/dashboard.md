---
created: 2026-07-06
tags: [dashboard]
---

# 대시보드

## 진행 중인 프로젝트
```dataview
TABLE status, stack, github
FROM "03-projects"
WHERE status = "active"
SORT created DESC
```

## 최근 7일 일일 노트
```dataview
LIST
FROM "02-calendar"
SORT created DESC
LIMIT 7
```

## 미해결 에러
```dataview
TABLE project, created
FROM "03-projects"
WHERE contains(tags, "error") AND status != "resolved"
SORT created DESC
```

## 면접 기록
```dataview
TABLE company, date, result
FROM "03-projects/job-search"
WHERE contains(tags, "interview")
SORT date DESC
```
