from pathlib import Path
from origin_cli.generators.extension.base import AbstractGenerator
from origin_cli.generators.extension.context import ExtensionContext

class TestsGenerator(AbstractGenerator):
    def generate(self, context: ExtensionContext, base_dir: Path) -> None:
        tests_dir = base_dir / "tests"
        tests_dir.mkdir(parents=True, exist_ok=True)
        
        tests_path = tests_dir / "extension-test.yaml"
        tests_path.write_text(f"""name: {context.name} Extension Validation
description: "Validates the generated {context.name} extension structure"

tests:
  - name: "Required files exist"
    assert:
      exists: "origin-extension.yaml"
      
  - name: "Manifest is valid YAML"
    assert:
      valid_yaml: "origin-extension.yaml"
""")
