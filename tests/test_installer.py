import pytest
import json
from pathlib import Path
from origin_cli.installer.file_utils import copy_directory, merge_json
from origin_cli.installer.models import InstallContext, InstallResult
from origin_cli.installer.github_installers import GitHubSkillInstaller
from origin_cli.installer.mcp_installer import McpInstaller

@pytest.fixture
def temp_workspace(tmp_path):
    # Setup mock extension source
    src = tmp_path / "dummy-ext"
    src.mkdir()
    
    (src / "origin-extension.yaml").write_text("name: dummy\nversion: 1.0.0")
    
    # Mock github skills
    (src / "github" / "skills").mkdir(parents=True)
    (src / "github" / "skills" / "skill1.md").write_text("skill1")
    
    # Mock mcp
    (src / "mcp").mkdir(parents=True)
    mcp_config = {
        "mcpServers": {
            "dummy": {"command": "echo"}
        }
    }
    with open(src / "mcp" / "github.json", "w") as f:
        json.dump(mcp_config, f)
        
    # Setup mock project target
    project = tmp_path / "project"
    project.mkdir()
    
    return src, project

def test_copy_directory_no_conflict(temp_workspace):
    src, project = temp_workspace
    
    added, replaced, skipped, errors = copy_directory(
        src / "github" / "skills", 
        project / ".github" / "skills"
    )
    
    assert len(added) == 1
    assert len(replaced) == 0
    assert len(skipped) == 0
    assert (project / ".github" / "skills" / "skill1.md").exists()

def test_copy_directory_conflict_skip(temp_workspace):
    src, project = temp_workspace
    
    # Pre-create conflict
    target = project / ".github" / "skills"
    target.mkdir(parents=True)
    (target / "skill1.md").write_text("existing")
    
    added, replaced, skipped, errors = copy_directory(src / "github" / "skills", target, force=False)
    
    assert len(added) == 0
    assert len(replaced) == 0
    assert len(skipped) == 1
    assert (target / "skill1.md").read_text() == "existing"

def test_copy_directory_conflict_force(temp_workspace):
    src, project = temp_workspace
    
    # Pre-create conflict
    target = project / ".github" / "skills"
    target.mkdir(parents=True)
    (target / "skill1.md").write_text("existing")
    
    added, replaced, skipped, errors = copy_directory(src / "github" / "skills", target, force=True)
    
    assert len(added) == 0
    assert len(replaced) == 1
    assert len(skipped) == 0
    assert (target / "skill1.md").read_text() == "skill1"

def test_merge_json_no_conflict(temp_workspace):
    src, project = temp_workspace
    
    added, replaced, skipped, errors = merge_json(
        src / "mcp" / "github.json",
        project / ".vscode" / "mcp.json"
    )
    
    assert len(added) == 1
    assert len(skipped) == 0
    
    with open(project / ".vscode" / "mcp.json") as f:
        data = json.load(f)
        assert "dummy" in data["mcpServers"]

def test_merge_json_conflict_skip(temp_workspace):
    src, project = temp_workspace
    
    # Pre-create conflict
    target = project / ".vscode" / "mcp.json"
    target.parent.mkdir(parents=True)
    with open(target, "w") as f:
        json.dump({"mcpServers": {"dummy": {"command": "existing"}}}, f)
        
    added, replaced, skipped, errors = merge_json(src / "mcp" / "github.json", target, force=False)
    
    assert len(skipped) == 1
    assert len(replaced) == 0
    
    with open(target) as f:
        data = json.load(f)
        assert data["mcpServers"]["dummy"]["command"] == "existing"

def test_installer_abstraction(temp_workspace, monkeypatch):
    src, project = temp_workspace
    
    # Mock Path.cwd() to return our mock project
    monkeypatch.setattr(Path, "cwd", lambda: project)
    
    context = InstallContext(
        extension_source_path=src,
        extension_name="dummy",
        manifest={"name": "dummy"},
    )
    context.managed_dir = src
    
    installer = GitHubSkillInstaller()
    res = installer.install(context)
    
    assert res.is_success()
    assert len(res.added) == 1
    assert res.installer_name == "GitHub Skills"

def test_remove_json_keys(temp_workspace):
    src, project = temp_workspace
    
    target = project / ".vscode" / "mcp.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(target, "w") as f:
        json.dump({"mcpServers": {"dummy": {"command": "echo"}, "other": {"command": "ls"}}}, f)
        
    from origin_cli.installer.file_utils import remove_json_keys
    removed, errors = remove_json_keys(target, ["dummy"])
    
    assert len(removed) == 1
    assert "dummy" in removed
    
    with open(target) as f:
        data = json.load(f)
        assert "dummy" not in data["mcpServers"]
        assert "other" in data["mcpServers"]

def test_speckit_wrapper_abort(monkeypatch):
    import subprocess
    from origin_cli.installer.speckit_wrapper import SpecKitWrapper
    
    def mock_run(*args, **kwargs):
        raise subprocess.CalledProcessError(1, cmd="specify")
        
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    # Should safely catch the error and return False, not throw unhandled exception
    assert SpecKitWrapper.add(Path("dummy")) is False
