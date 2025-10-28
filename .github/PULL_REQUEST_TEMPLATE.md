# Pull Request

## Description

### What does this PR do?

A clear and concise summary of the changes and their purpose.

### Why is this change needed?

Explain the motivation and context for this change.

## Type of Change

What type of change does this PR introduce? (Check all that apply)

- [ ] 🐛 **Bug fix** (non-breaking change that fixes an issue)
- [ ] ✨ **New feature** (non-breaking change that adds functionality)
- [ ] 💥 **Breaking change** (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 **Documentation** (updates to documentation only)
- [ ] 🎨 **Style** (formatting, missing semicolons, etc.; no code change)
- [ ] ♻️ **Refactoring** (code change that neither fixes a bug nor adds a feature)
- [ ] ⚡ **Performance** (code change that improves performance)
- [ ] ✅ **Test** (adding missing tests or correcting existing tests)
- [ ] 🔧 **Chore** (changes to build process, dependencies, or auxiliary tools)
- [ ] 🚀 **CI/CD** (changes to CI/CD configuration or workflows)

## Related Issues

Closes #(issue number)
Fixes #(issue number)
Relates to #(issue number)

## Changes Made

### Backend Changes (if applicable)
- Brief description of backend changes
- API endpoints added/modified
- Database migrations
- Service logic updates

### Frontend Changes (if applicable)
- Brief description of frontend changes
- UI/UX updates
- New screens or components
- State management changes

### Infrastructure/DevOps Changes (if applicable)
- Docker configuration updates
- CI/CD pipeline changes
- Deployment scripts modifications

## Testing

### How has this been tested?

Describe the tests you ran and how to reproduce them:

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] E2E tests

### Test Configuration

- **Backend**: Python version, database version
- **Frontend**: Flutter version, test devices
- **Environment**: Local / Docker / Staging

### Test Evidence

Add screenshots, logs, or test output here:

```
Paste relevant test output or logs
```

## Checklist

### Code Quality

- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] My changes generate no new warnings or errors
- [ ] No linter errors introduced

### Testing

- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Backend test coverage meets minimum threshold (85%)
- [ ] Frontend tests pass (`flutter test`)

### Documentation

- [ ] I have updated the documentation accordingly
- [ ] I have added/updated docstrings for new functions and classes
- [ ] I have updated the README if needed
- [ ] I have documented any new environment variables or configuration

### CI/CD

- [ ] All CI checks are passing
- [ ] Backend linting passed (Ruff/Flake8)
- [ ] Frontend analysis passed (`flutter analyze`)
- [ ] No merge conflicts with target branch

### Breaking Changes (if applicable)

- [ ] I have documented breaking changes in the PR description
- [ ] I have updated the migration guide
- [ ] I have bumped the major version (or noted it should be done)
- [ ] I have communicated breaking changes to stakeholders

## Screenshots (if applicable)

### Before
[Add screenshots showing the state before your changes]

### After
[Add screenshots showing the state after your changes]

## Performance Impact

Does this change affect performance?

- [ ] No performance impact
- [ ] Performance improved
- [ ] Performance may be degraded (explain below)

**Details:**

## Security Considerations

Does this change have security implications?

- [ ] No security impact
- [ ] Security improvement
- [ ] Potential security risk (explain below and tag security team)

**Details:**

## Deployment Notes

Are there special steps needed for deployment?

- [ ] No special deployment steps
- [ ] Database migration required (see migrations/)
- [ ] Environment variables need to be added/updated
- [ ] Configuration changes required
- [ ] Data migration or seeding needed

**Instructions:**

## Rollback Plan

How can this change be rolled back if needed?

## Additional Context

Add any other context, links, or information about the PR here:

- Links to design documents
- Related Slack/email discussions
- Academic references (for medical content)
- Performance benchmarks

## Reviewer Notes

**Specific areas to focus on during review:**

1. 
2. 
3. 

---

**Checklist for Reviewers:**

- [ ] Code changes are clear and well-structured
- [ ] Tests adequately cover the changes
- [ ] Documentation is sufficient
- [ ] No obvious security issues
- [ ] Performance implications considered
- [ ] Breaking changes properly documented
