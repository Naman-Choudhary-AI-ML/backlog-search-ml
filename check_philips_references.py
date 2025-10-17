"""
Check for any Philips references in the codebase before GitHub upload.
This ensures the repository is completely sanitized and safe to publish.
"""

import os
import re
from pathlib import Path

# Patterns to search for
SENSITIVE_PATTERNS = [
    r'\bPhilips\b',
    r'\bphilips\b',
    r'\bPHILIPS\b',
    r'\bCSL\b',  # Philips CSL
    r'\bcsl\b',
]

# Directories and files to check
INCLUDE_EXTENSIONS = ['.py', '.md', '.txt', '.yaml', '.yml', '.json', '.csv']
EXCLUDE_DIRS = ['.git', '__pycache__', 'mlruns', '.cache', 'venv', 'env']
EXCLUDE_FILES = ['check_philips_references.py', 'SPOTLIGHT_PROJECT_DOCUMENTATION.md']

def should_check_file(file_path):
    """Check if file should be scanned"""
    # Check extension
    if not any(str(file_path).endswith(ext) for ext in INCLUDE_EXTENSIONS):
        return False

    # Check if in excluded directory
    parts = file_path.parts
    if any(excluded in parts for excluded in EXCLUDE_DIRS):
        return False

    # Check if excluded file
    if file_path.name in EXCLUDE_FILES:
        return False

    return True

def scan_file(file_path):
    """Scan a file for sensitive patterns"""
    matches = []

    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                for pattern in SENSITIVE_PATTERNS:
                    if re.search(pattern, line):
                        matches.append({
                            'file': str(file_path),
                            'line': line_num,
                            'content': line.strip(),
                            'pattern': pattern
                        })
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return matches

def main():
    """Main scanning function"""
    print("="*80)
    print("PHILIPS REFERENCE CHECKER")
    print("="*80)
    print("\nScanning for sensitive references...\n")

    root_dir = Path(__file__).parent
    all_matches = []
    files_scanned = 0

    # Scan all files
    for file_path in root_dir.rglob('*'):
        if file_path.is_file() and should_check_file(file_path):
            files_scanned += 1
            matches = scan_file(file_path)
            all_matches.extend(matches)

    # Report results
    print(f"Files scanned: {files_scanned}")
    print(f"Sensitive references found: {len(all_matches)}\n")

    if all_matches:
        print("⚠️  WARNING: Sensitive references found!")
        print("="*80)

        for match in all_matches:
            print(f"\nFile: {match['file']}")
            print(f"Line {match['line']}: {match['content']}")
            print(f"Pattern: {match['pattern']}")

        print("\n" + "="*80)
        print("❌ REPOSITORY NOT SAFE FOR GITHUB")
        print("Please remove all Philips references before uploading.")
        return 1
    else:
        print("="*80)
        print("✅ NO SENSITIVE REFERENCES FOUND")
        print("Repository is safe for GitHub upload!")
        print("="*80)
        return 0

if __name__ == "__main__":
    exit(main())
