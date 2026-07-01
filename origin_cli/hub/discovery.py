import json
import re
from pathlib import Path


def detect_tech_stack(project_dir: Path) -> list[str]:
    """
    Scans the project directory quickly for common files (package.json, pyproject.toml)
    and returns a list of detected technology tags (e.g., ['react', 'typescript', 'python']).
    """
    tags = set()

    # 1. Check Node.js ecosystem
    pkg_json = project_dir / "package.json"
    if pkg_json.exists():
        tags.add("node")
        try:
            data = json.loads(pkg_json.read_text())
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            
            if "react" in deps: tags.add("react")
            if "vue" in deps: tags.add("vue")
            if "next" in deps: tags.add("next.js")
            if "typescript" in deps: tags.add("typescript")
            if "tailwindcss" in deps: tags.add("tailwindcss")
            if "jest" in deps: tags.add("jest")
            if "vitest" in deps: tags.add("vitest")
            if "express" in deps: tags.add("express")
            
        except Exception:
            pass

    # 2. Check Python ecosystem
    pyproject = project_dir / "pyproject.toml"
    requirements = project_dir / "requirements.txt"
    if pyproject.exists() or requirements.exists():
        tags.add("python")
        
        # very rudimentary check by reading raw text for common frameworks
        content = ""
        if pyproject.exists():
            content += pyproject.read_text().lower()
        if requirements.exists():
            content += requirements.read_text().lower()
            
        if "fastapi" in content: tags.add("fastapi")
        if "django" in content: tags.add("django")
        if "flask" in content: tags.add("flask")
        if "pytest" in content: tags.add("pytest")
        if "pydantic" in content: tags.add("pydantic")

    # 3. Check Go
    if (project_dir / "go.mod").exists():
        tags.add("go")

    # 4. Check Rust
    if (project_dir / "Cargo.toml").exists():
        tags.add("rust")
        
    return sorted(list(tags))
