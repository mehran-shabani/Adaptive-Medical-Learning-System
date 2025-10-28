#!/usr/bin/env python3
"""
Changelog Generator from Git Commits

This script generates a changelog from git commits between two references
(typically the last tag and HEAD). It parses conventional commit messages
and organizes them into categories.

Usage:
    python changelog_from_commits.py <from_ref> <to_ref>
    python changelog_from_commits.py v1.0.5 HEAD
"""

import re
import subprocess
import sys
from collections import defaultdict
from typing import List, Dict, Tuple


class CommitParser:
    """Parse conventional commit messages."""
    
    # Conventional commit pattern: type(scope): subject
    COMMIT_PATTERN = re.compile(
        r'^(?P<type>\w+)(?:\((?P<scope>[\w-]+)\))?: (?P<subject>.+)$'
    )
    
    # Commit types and their display names
    COMMIT_TYPES = {
        'feat': '✨ Features',
        'fix': '🐛 Bug Fixes',
        'docs': '📝 Documentation',
        'style': '💄 Styles',
        'refactor': '♻️ Code Refactoring',
        'perf': '⚡ Performance Improvements',
        'test': '✅ Tests',
        'build': '👷 Build System',
        'ci': '🔧 CI/CD',
        'chore': '🔨 Chores',
        'revert': '⏪ Reverts',
    }
    
    def __init__(self):
        """Initialize commit parser."""
        self.commits_by_type = defaultdict(list)
        self.breaking_changes = []
    
    def parse_commit(self, commit_hash: str, commit_message: str) -> None:
        """
        Parse a single commit message and categorize it.
        
        Args:
            commit_hash: Short git commit hash
            commit_message: Full commit message (first line)
        """
        # Check for breaking change marker
        is_breaking = 'BREAKING CHANGE' in commit_message or commit_message.startswith('!')
        
        # Try to parse as conventional commit
        match = self.COMMIT_PATTERN.match(commit_message)
        
        if match:
            commit_type = match.group('type')
            scope = match.group('scope')
            subject = match.group('subject')
            
            # Format the commit entry
            if scope:
                entry = f"**{scope}**: {subject} ({commit_hash})"
            else:
                entry = f"{subject} ({commit_hash})"
            
            # Add to appropriate category
            self.commits_by_type[commit_type].append(entry)
            
            # Track breaking changes separately
            if is_breaking:
                self.breaking_changes.append(entry)
        else:
            # Non-conventional commit - add to "Other Changes"
            entry = f"{commit_message} ({commit_hash})"
            self.commits_by_type['other'].append(entry)
    
    def generate_changelog(self) -> str:
        """
        Generate formatted changelog from parsed commits.
        
        Returns:
            Markdown-formatted changelog string
        """
        sections = []
        
        # Breaking changes section (if any)
        if self.breaking_changes:
            sections.append("## ⚠️ BREAKING CHANGES\n")
            for change in self.breaking_changes:
                sections.append(f"- {change}")
            sections.append("")
        
        # Regular commit sections
        for commit_type, display_name in self.COMMIT_TYPES.items():
            commits = self.commits_by_type.get(commit_type, [])
            if commits:
                sections.append(f"## {display_name}\n")
                for commit in commits:
                    sections.append(f"- {commit}")
                sections.append("")
        
        # Other changes (non-conventional commits)
        other_commits = self.commits_by_type.get('other', [])
        if other_commits:
            sections.append("## 📦 Other Changes\n")
            for commit in other_commits:
                sections.append(f"- {commit}")
            sections.append("")
        
        return "\n".join(sections)


def get_commits_between(from_ref: str, to_ref: str) -> List[Tuple[str, str]]:
    """
    Get list of commits between two git references.
    
    Args:
        from_ref: Starting git reference (e.g., tag name)
        to_ref: Ending git reference (e.g., 'HEAD')
    
    Returns:
        List of tuples containing (commit_hash, commit_message)
    """
    try:
        # Get commit log with format: <short_hash>|<subject>
        cmd = [
            'git', 'log',
            f'{from_ref}..{to_ref}',
            '--pretty=format:%h|%s',
            '--no-merges'  # Exclude merge commits
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        
        commits = []
        for line in result.stdout.strip().split('\n'):
            if '|' in line:
                commit_hash, message = line.split('|', 1)
                commits.append((commit_hash, message))
        
        return commits
        
    except subprocess.CalledProcessError as e:
        print(f"Error getting git commits: {e}", file=sys.stderr)
        print(f"Make sure you're in a git repository and refs exist", file=sys.stderr)
        sys.exit(1)


def get_latest_tag() -> str:
    """
    Get the latest git tag.
    
    Returns:
        Latest tag name, or None if no tags exist
    """
    try:
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None


def main():
    """Main entry point for changelog generation."""
    # Parse command line arguments
    if len(sys.argv) < 2:
        # No arguments - try to use latest tag to HEAD
        from_ref = get_latest_tag()
        if not from_ref:
            print("Error: No tags found and no range specified", file=sys.stderr)
            print("Usage: python changelog_from_commits.py <from_ref> <to_ref>", file=sys.stderr)
            sys.exit(1)
        to_ref = 'HEAD'
        print(f"No range specified, using {from_ref}..HEAD", file=sys.stderr)
    elif len(sys.argv) == 3:
        from_ref = sys.argv[1]
        to_ref = sys.argv[2]
    else:
        print("Usage: python changelog_from_commits.py <from_ref> <to_ref>", file=sys.stderr)
        sys.exit(1)
    
    # Get commits in range
    commits = get_commits_between(from_ref, to_ref)
    
    if not commits:
        print(f"No commits found between {from_ref} and {to_ref}", file=sys.stderr)
        print("\n## No Changes\n\nNo commits in this release.")
        sys.exit(0)
    
    # Parse commits and generate changelog
    parser = CommitParser()
    for commit_hash, commit_message in commits:
        parser.parse_commit(commit_hash, commit_message)
    
    changelog = parser.generate_changelog()
    
    # Output changelog
    if not changelog.strip():
        print("## Changes\n\nMinor updates and improvements.")
    else:
        print(changelog)
    
    sys.exit(0)


if __name__ == "__main__":
    main()
