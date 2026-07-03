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
        
    # 5. Check Java / JVM (Maven or Gradle)
    pom_xml = project_dir / "pom.xml"
    build_gradle = project_dir / "build.gradle"
    build_gradle_kts = project_dir / "build.gradle.kts"
    if pom_xml.exists() or build_gradle.exists() or build_gradle_kts.exists():
        tags.add("java")
        
        # Check for Spring Boot
        content = ""
        if pom_xml.exists(): content += pom_xml.read_text().lower()
        if build_gradle.exists(): content += build_gradle.read_text().lower()
        if build_gradle_kts.exists(): content += build_gradle_kts.read_text().lower()
        if "spring-boot" in content or "springframework" in content:
            tags.add("spring-boot")

    # 6. Check Ruby
    if (project_dir / "Gemfile").exists():
        tags.add("ruby")
        if "rails" in (project_dir / "Gemfile").read_text().lower():
            tags.add("rails")

    # 7. Check PHP
    if (project_dir / "composer.json").exists():
        tags.add("php")
        try:
            php_data = json.loads((project_dir / "composer.json").read_text())
            php_deps = str(php_data.get("require", {}))
            if "laravel" in php_deps: tags.add("laravel")
            if "symfony" in php_deps: tags.add("symfony")
        except Exception:
            pass

    # 8. Check C# / .NET
    if list(project_dir.glob("*.csproj")) or list(project_dir.glob("*.sln")):
        tags.add("csharp")
        tags.add("dotnet")

    # 9. Check C++
    if (project_dir / "CMakeLists.txt").exists() or (project_dir / "Makefile").exists():
        tags.add("cpp")

    return sorted(list(tags))
