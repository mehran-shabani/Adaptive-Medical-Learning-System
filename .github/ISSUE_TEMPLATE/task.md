---
name: Technical Task
about: Track a specific technical task or chore
title: '[TASK] '
labels: tech-debt
assignees: ''
---

## Task Description

A clear and concise description of the technical task to be completed.

## Context

**Why is this task needed?**

Explain the background, motivation, or problem this task addresses:
- Is this technical debt?
- Is this a prerequisite for another feature?
- Is this an optimization or refactoring?
- Is this infrastructure or DevOps work?

## Scope

**What needs to be done?**

List specific actions or changes required:

1. [ ] Action item 1
2. [ ] Action item 2
3. [ ] Action item 3

## Affected Components

**Which parts of the codebase will change?**

- [ ] Backend API
- [ ] Frontend (Flutter)
- [ ] Database schema
- [ ] CI/CD pipelines
- [ ] Documentation
- [ ] Infrastructure/DevOps
- [ ] Tests

**Specific files/modules:**
- `path/to/file1.py`
- `path/to/file2.dart`

## Definition of Done

**How will we know this task is complete?**

- [ ] All code changes implemented
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Code reviewed and approved
- [ ] CI/CD checks passing
- [ ] Deployed to staging (if applicable)
- [ ] No new linter warnings introduced

## Testing Strategy

**How will this be tested?**

- Unit tests for [specific functionality]
- Integration tests for [specific flows]
- Manual testing steps: [list steps]

## Dependencies

**What does this task depend on?**

- [ ] Issue #XXX must be completed first
- [ ] External library upgrade needed
- [ ] Database migration required
- [ ] Configuration changes needed

**What depends on this task?**

- Issue #YYY is blocked by this task
- Feature ZZZ requires this to be done first

## Related Issues/PRs

- Related to #XXX
- Blocks #YYY
- Depends on #ZZZ

## Estimated Effort

**Your estimate of time required:**

- [ ] Small (< 2 hours)
- [ ] Medium (2-8 hours)
- [ ] Large (1-3 days)
- [ ] Extra Large (> 3 days)

## Technical Notes

**Implementation details, gotchas, or considerations:**

```
Add any code snippets, API signatures, or technical specifications here
```

## Checklist

- [ ] I have clearly described what needs to be done
- [ ] I have identified affected components
- [ ] I have defined what "done" means
- [ ] I have noted any dependencies or blockers
