#!/usr/bin/env python3
"""
Version Bumping Script with Custom Patch Increment Logic

This script implements semantic versioning with a special patch increment rule:
- Patches increment by 0.01 (e.g., 1.0.01, 1.0.02, ..., 1.0.99)
- When patch reaches 99, it rolls over to the next minor version
- Usage: python bump_version.py [major|minor|patch]

Default behavior: bump patch
"""

import sys
from pathlib import Path
from typing import Tuple


class VersionBumper:
    """Handles version bumping with custom patch increment logic."""

    def __init__(self, version_file: Path = None):
        """Initialize version bumper with version file path."""
        if version_file is None:
            # Default to VERSION file in repository root
            repo_root = Path(__file__).parent.parent.parent
            version_file = repo_root / "VERSION"
        
        self.version_file = version_file
        self.major, self.minor, self.patch = self._read_version()

    def _read_version(self) -> Tuple[int, int, int]:
        """Read current version from VERSION file."""
        if not self.version_file.exists():
            raise FileNotFoundError(f"VERSION file not found at {self.version_file}")
        
        version_string = self.version_file.read_text().strip()
        return self._parse_version(version_string)

    def _parse_version(self, version_string: str) -> Tuple[int, int, int]:
        """Parse version string into major, minor, patch components."""
        try:
            parts = version_string.split(".")
            if len(parts) != 3:
                raise ValueError("Version must have exactly 3 parts")
            
            major = int(parts[0])
            minor = int(parts[1])
            patch = int(parts[2])
            
            return major, minor, patch
        except (ValueError, IndexError) as e:
            raise ValueError(f"Invalid version format '{version_string}': {e}")

    def bump_major(self) -> str:
        """
        Bump major version and reset minor and patch to 0.
        Example: 1.2.15 -> 2.0.0
        """
        self.major += 1
        self.minor = 0
        self.patch = 0
        return self._format_version()

    def bump_minor(self) -> str:
        """
        Bump minor version and reset patch to 0.
        Example: 1.2.15 -> 1.3.0
        """
        self.minor += 1
        self.patch = 0
        return self._format_version()

    def bump_patch(self) -> str:
        """
        Bump patch version with custom increment logic.
        
        - Increments by 1 (displayed as 0.01 in version)
        - When patch reaches 99, rolls over to next minor version
        
        Examples:
            1.0.0  -> 1.0.01
            1.0.01 -> 1.0.02
            1.0.98 -> 1.0.99
            1.0.99 -> 1.1.0  (rollover)
        """
        self.patch += 1
        
        # Check for rollover at 99
        if self.patch > 99:
            self.minor += 1
            self.patch = 0
        
        return self._format_version()

    def _format_version(self) -> str:
        """
        Format version string with proper patch formatting.
        
        - If patch is 0: major.minor.0
        - If patch is 1-9: major.minor.0X
        - If patch is 10-99: major.minor.XX
        """
        if self.patch == 0:
            return f"{self.major}.{self.minor}.0"
        else:
            # Format patch with leading zero for 1-9
            patch_str = f"{self.patch:02d}"
            return f"{self.major}.{self.minor}.{patch_str}"

    def write_version(self, new_version: str) -> None:
        """Write new version to VERSION file."""
        self.version_file.write_text(new_version + "\n")

    def get_current_version(self) -> str:
        """Get current version as formatted string."""
        return self._format_version()


def main():
    """Main entry point for version bumping."""
    # Determine bump type from command line argument
    bump_type = sys.argv[1].lower() if len(sys.argv) > 1 else "patch"
    
    if bump_type not in ["major", "minor", "patch"]:
        print(f"Error: Invalid bump type '{bump_type}'", file=sys.stderr)
        print("Usage: python bump_version.py [major|minor|patch]", file=sys.stderr)
        sys.exit(1)
    
    try:
        bumper = VersionBumper()
        
        # Get current version for logging
        current_version = bumper.get_current_version()
        print(f"Current version: {current_version}", file=sys.stderr)
        
        # Bump version based on type
        if bump_type == "major":
            new_version = bumper.bump_major()
        elif bump_type == "minor":
            new_version = bumper.bump_minor()
        else:  # patch
            new_version = bumper.bump_patch()
        
        # Write new version to file
        bumper.write_version(new_version)
        
        print(f"Bumped {bump_type} version: {current_version} -> {new_version}", file=sys.stderr)
        
        # Output new version to stdout (for capturing in CI/CD)
        print(new_version)
        
        sys.exit(0)
        
    except Exception as e:
        print(f"Error bumping version: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
