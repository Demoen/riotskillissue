
import re
from pathlib import Path
import sys
import os

def bump_version():
    target_file = Path("pyproject.toml")
    content = target_file.read_text(encoding="utf-8")
    
    # improved regex to match version = "x.y.z"
    pattern = r'version\s*=\s*"(\d+)\.(\d+)\.(\d+)"'
    match = re.search(pattern, content)
    
    if not match:
        print("Could not find version in pyproject.toml")
        sys.exit(1)
        
    major, minor, patch = map(int, match.groups())
    new_patch = patch + 1
    new_version = f"{major}.{minor}.{new_patch}"
    
    new_content = re.sub(pattern, f'version = "{new_version}"', content)
    target_file.write_text(new_content, encoding="utf-8")
    
    print(f"Bumped version from {major}.{minor}.{patch} to {new_version}")
    
    # Store verifyable output for GitHub Actions
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a") as f:
            f.write(f"new_version={new_version}\n")
    else:
        # Print for local debugging or older runners
        print(f"::set-output name=new_version::{new_version}")

if __name__ == "__main__":
    bump_version()
