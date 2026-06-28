import pytest
import yaml
from pathlib import Path
from origin_cli.generators.preset.builder import PresetBuilder
from origin_cli.generators.preset.manifest import PresetManifestGenerator
from origin_cli.generators.preset.docs import PresetDocsGenerator
from origin_cli.generators.preset.speckit_assets import SpecKitAssetsGenerator

def test_preset_generator(tmp_path):
    context = {
        "name": "test-preset",
        "version": "1.2.3",
        "description": "Test",
        "author": "Alice",
        "license": "MIT"
    }
    
    generators = [
        PresetManifestGenerator(),
        PresetDocsGenerator(),
        SpecKitAssetsGenerator()
    ]
    
    builder = PresetBuilder(generators)
    output_dir = tmp_path / "test-preset"
    
    builder.build(context, output_dir)
    
    assert (output_dir / "origin-preset.yaml").exists()
    assert (output_dir / "README.md").exists()
    
    # Check Spec Kit assets
    assert (output_dir / "speckit" / "preset" / "commands" / "specify.md").exists()
    assert (output_dir / "speckit" / "preset" / "templates" / "plan.md").exists()
    assert (output_dir / "speckit" / "preset" / "scripts" / "pre-plan.sh").exists()
    
    # Check Manifest content
    with open(output_dir / "origin-preset.yaml", "r") as f:
        data = yaml.safe_load(f)
        
    assert data["name"] == "test-preset"
    assert data["version"] == "1.2.3"
    assert "speckit" in data
    assert "preset" in data["speckit"]
    assert "commands" in data["speckit"]["preset"]
