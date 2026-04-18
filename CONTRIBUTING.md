# AI in Production - Final project - Group 9

## Team members

| No  | Student ID | Student Name        | Role        |
| --- | ---------- | ------------------- | ----------- |
| 1   | 25MSA23226 | Hồ Nhật Thanh       | Team Leader |
| 2   | 25MSA23250 | Bùi Nguyễn Trúc Như | Team member |
| 3   | 25MSA23239 | Nguyễn Văn Nhật     | Team member |

## Task List
| No  | Task                              | Assignee | Status      |
| --- | --------------------------------- | -------- | ----------- |
| 1   | Problem Definition & Requirements | Thanh    | Done        |
| 2   | System Design & Architecture      | Thanh    | Done        |
| 3   | ML Pipeline                       | Như      | In Progress |
| 4   | Deployment                        | Như      | In Progress |
| 5   | Monitoring                        | Nhật     | In Progress |
| 6   | Testing & CI/CD                   | Nhật     | In Progress |
| 7   | Responsible AI                    | Nhật     | In Progress |
| 8   | Documentation                     | Thanh    | In Progress |

## 3. Branch Strategy

- `dev`: integration branch for ongoing development
- `staging`: pre-release validation branch
- `main`: release branch

Expected merge flow:
1. `dev -> staging`
2. `staging -> main`

## 4. CI Rules

Workflow: `.github/workflows/CICD.yml`

- Push on `staging` or `main`: run tests
- Pull request `dev -> staging`: run tests + build staging-tagged image
- Pull request `staging -> main`: run tests + build main-tagged image

## 5. Commit and PR Conventions

- Use clear commit messages describing scope and impact.
- Keep PRs small and focused.
- Include test evidence for behavior changes.
- Include screenshots for monitoring/dashboard changes.

## 6. Local Development Steps

```bash
# 1) Start stack
docker compose up -d --build

# 2) Run API checks
curl http://localhost:8000/health

# 3) Run tests (python 3.10 recommended)
python -m pytest tests/ -v
```

## 7. Ownership Notes

- Do not overwrite files owned by another scope without discussion.
- For shared files, coordinate in PR description before merge.
