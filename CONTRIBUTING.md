# Contributing to Adaptive Learning Platform

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Workflow](#development-workflow)
- [Branch Naming Convention](#branch-naming-convention)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Quality Standards](#code-quality-standards)
- [Testing Requirements](#testing-requirements)

## Code of Conduct

This project adheres to a [Code of Conduct](./CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

## How Can I Contribute?

### Reporting Bugs

- **Use the bug report template** when creating a new issue
- **Search existing issues** to avoid duplicates
- **Include detailed information**:
  - Steps to reproduce
  - Expected vs. actual behavior
  - Screenshots (if applicable)
  - Version information
  - Environment details (OS, browser, etc.)

### Suggesting Features

- **Use the feature request template** when proposing new features
- **Explain the problem** your feature would solve
- **Describe the solution** clearly
- **Consider the impact** on existing users and system performance

### Submitting Code Changes

1. Fork the repository
2. Create a feature branch (see naming convention below)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Submit a pull request

## Development Workflow

### Initial Setup

```bash
# Clone your fork
git clone https://github.com/your-username/repo-name.git
cd repo-name

# Add upstream remote
git remote add upstream https://github.com/original-org/repo-name.git

# Install dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && flutter pub get
```

### Staying in Sync

```bash
# Fetch latest changes from upstream
git fetch upstream

# Merge upstream main into your local main
git checkout main
git merge upstream/main

# Push to your fork
git push origin main
```

## Branch Naming Convention

Use descriptive branch names following these patterns:

- **Features**: `feature/<short-description>`
  - Example: `feature/quiz-timer`, `feature/dark-mode`
  
- **Bug Fixes**: `fix/<bug-description>`
  - Example: `fix/login-validation`, `fix/memory-leak`
  
- **Infrastructure/DevOps**: `infra/<change-description>`
  - Example: `infra/docker-optimization`, `infra/ci-speedup`
  
- **Documentation**: `docs/<topic>`
  - Example: `docs/api-reference`, `docs/deployment-guide`
  
- **Chores/Maintenance**: `chore/<task>`
  - Example: `chore/dependency-update`, `chore/refactor-utils`

## Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation only changes
- **style**: Code style changes (formatting, missing semicolons, etc.)
- **refactor**: Code change that neither fixes a bug nor adds a feature
- **perf**: Performance improvement
- **test**: Adding or updating tests
- **chore**: Maintenance tasks, dependency updates
- **ci**: CI/CD configuration changes

### Examples

```
feat(quiz): add timer functionality to quiz interface

Add a countdown timer that displays remaining time for each quiz question.
Timer pauses when user navigates away and resumes on return.

Closes #123
```

```
fix(auth): resolve token expiration handling

Properly refresh authentication tokens before they expire.
Prevents users from being unexpectedly logged out during sessions.

Fixes #456
```

## Pull Request Process

### Before Submitting

1. ✅ **All tests pass locally**
   ```bash
   # Backend
   cd backend && pytest --cov=app --cov-report=term-missing
   
   # Frontend
   cd frontend && flutter test
   ```

2. ✅ **Linting passes**
   ```bash
   # Backend
   ruff check .
   
   # Frontend
   flutter analyze
   ```

3. ✅ **Code coverage meets minimum threshold** (85% for backend)

4. ✅ **Update documentation** if you changed APIs or added features

5. ✅ **Add or update tests** for your changes

### Submitting the PR

1. **Use the Pull Request template** provided
2. **Link related issues** using keywords (e.g., "Closes #123")
3. **Provide context** in the PR description
4. **Mark as draft** if work is not complete
5. **Request review** from at least one maintainer

### PR Review Checklist

Your PR will be reviewed for:

- [ ] Code quality and adherence to project style
- [ ] Test coverage (new code must be tested)
- [ ] Documentation updates (if applicable)
- [ ] No breaking changes (or properly documented if necessary)
- [ ] CI checks passing (lint, tests, coverage)
- [ ] Commit messages follow convention
- [ ] No merge conflicts with main branch

### After Approval

- **Squash merge**: We use squash merging for clean history
- **Automatic versioning**: Merging to `main` triggers automated version bump
- **Delete branch**: Remove your feature branch after merge

## Code Quality Standards

### Backend (Python)

- **Style Guide**: Follow PEP 8
- **Linting**: Use Ruff or Flake8 (configured in `pyproject.toml`)
- **Type Hints**: Use type annotations for function signatures
- **Docstrings**: Document all public functions, classes, and modules
- **Max Line Length**: 120 characters

Example:
```python
def calculate_mastery_score(
    correct_answers: int,
    total_questions: int,
    time_spent: float
) -> float:
    """
    Calculate mastery score based on quiz performance.
    
    Args:
        correct_answers: Number of correct answers
        total_questions: Total number of questions
        time_spent: Time spent on quiz in seconds
        
    Returns:
        Mastery score between 0.0 and 1.0
    """
    # Implementation
    pass
```

### Frontend (Dart/Flutter)

- **Style Guide**: Follow [Effective Dart](https://dart.dev/guides/language/effective-dart)
- **Linting**: Configured in `analysis_options.yaml`
- **Widget Organization**: Separate widgets into logical files
- **State Management**: Use Provider or specified state management solution
- **Comments**: Document complex business logic

Example:
```dart
/// Calculates the mastery percentage for display.
/// 
/// Returns a value between 0 and 100 representing the
/// student's mastery level in this topic.
double calculateMasteryPercentage(MasteryModel mastery) {
  return (mastery.score * 100).clamp(0.0, 100.0);
}
```

## Testing Requirements

### Backend Testing

- **Minimum Coverage**: 85% overall
- **Test Types**:
  - Unit tests for business logic
  - Integration tests for API endpoints
  - Database tests with fixtures
  
```python
# Example test structure
import pytest
from app.mastery.service import MasteryService

@pytest.fixture
def mastery_service():
    return MasteryService()

def test_mastery_calculation(mastery_service):
    score = mastery_service.calculate(correct=8, total=10)
    assert 0.0 <= score <= 1.0
    assert score == 0.8
```

### Frontend Testing

- **Test Types**:
  - Widget tests for UI components
  - Unit tests for business logic
  - Integration tests for critical flows

```dart
// Example widget test
testWidgets('MasteryCard displays correct percentage', (tester) async {
  final mastery = MasteryModel(score: 0.75, topic: 'Cardiology');
  
  await tester.pumpWidget(MaterialApp(
    home: MasteryCard(mastery: mastery),
  ));
  
  expect(find.text('75%'), findsOneWidget);
});
```

## CI/CD Pipeline

All PRs must pass CI checks before merge:

1. **Linting**: Code style must be consistent
2. **Tests**: All tests must pass
3. **Coverage**: Backend coverage must meet 85% threshold
4. **Build**: Frontend must build successfully

You can run CI checks locally:

```bash
# Backend CI simulation
cd backend
ruff check .
pytest --cov=app --cov-report=term-missing --cov-fail-under=85

# Frontend CI simulation
cd frontend
flutter analyze
flutter test
flutter build apk --debug  # Test build
```

## Questions?

If you have questions not covered in this guide:

1. Check existing [documentation](./README.md)
2. Search [closed issues](https://github.com/your-org/repo/issues?q=is%3Aissue+is%3Aclosed)
3. Open a [new issue](https://github.com/your-org/repo/issues/new/choose) with the question template

## License

By contributing, you agree that your contributions will be licensed under the same [MIT License](./LICENSE) that covers this project.

---

**Thank you for contributing!** 🎉
