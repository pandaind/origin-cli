import pytest
from pathlib import Path
from origin_cli.generators.extension.context import ExtensionContext
from origin_cli.generators.extension.builder import ExtensionBuilder
from origin_cli.generators.extension.manifest import ManifestGenerator
from origin_cli.generators.extension.docs import DocsGenerator

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

def test_context_capability_check():
    ctx = ExtensionContext("test", "desc", "author", "0.1", "MIT", {"skills", "mcp"})
    assert ctx.has_capability("skills") is True
    assert ctx.has_capability("commands") is False

def test_manifest_generator(temp_dir: Path):
    ctx = ExtensionContext("jira", "desc", "author", "0.1", "MIT", {"skills", "mcp"})
    gen = ManifestGenerator()
    gen.generate(ctx, temp_dir)
    
    manifest_path = temp_dir / "origin-extension.yaml"
    assert manifest_path.exists()
    
    content = manifest_path.read_text()
    assert "name: jira" in content
    assert "skills:" in content
    assert "mcp:" in content
    assert "hooks:" not in content

def test_docs_generator(temp_dir: Path):
    ctx = ExtensionContext("jira", "desc", "author", "0.1", "MIT")
    gen = DocsGenerator()
    gen.generate(ctx, temp_dir)
    
    assert (temp_dir / "README.md").exists()
    assert (temp_dir / "docs" / "overview.md").exists()
    assert (temp_dir / "examples" / "install.md").exists()

def test_builder(temp_dir: Path):
    ctx = ExtensionContext("jira", "desc", "author", "0.1", "MIT")
    builder = ExtensionBuilder([DocsGenerator()])
    builder.build(ctx, temp_dir)
    
    assert (temp_dir / "README.md").exists()
