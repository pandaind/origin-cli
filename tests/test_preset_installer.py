import pytest
import yaml
from pathlib import Path

def test_preset_registry(tmp_path, monkeypatch):
    # Mock cwd
    project = tmp_path / "project"
    project.mkdir()
    monkeypatch.setattr(Path, "cwd", lambda: project)
    
    from origin_cli.installer.preset_registry import PresetRegistry
    from origin_cli.installer.models import InstallContext
    
    registry = PresetRegistry()
    context = InstallContext(
        extension_source_path=Path("dummy"),
        extension_name="test-preset",
        manifest={"version": "1.0.0"}
    )
    # mock managed dir since we skip init
    context.managed_dir = Path("dummy")
    
    res = registry.register(context, "test-preset")
    
    assert res.is_success()
    
    registry_file = project / ".origin" / "presets.yaml"
    assert registry_file.exists()
    
    with open(registry_file) as f:
        data = yaml.safe_load(f)
        assert data["presets"][0]["name"] == "test-preset"
        assert data["presets"][0]["enabled"] is True
        assert data["presets"][0]["priority"] == 0

def test_preset_speckit_wrapper_abort(monkeypatch):
    import subprocess
    from origin_cli.installer.speckit_wrapper import SpecKitWrapper
    
    def mock_run(*args, **kwargs):
        raise subprocess.CalledProcessError(1, cmd="specify")
        
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    assert SpecKitWrapper.preset_add(Path("dummy")) is False
