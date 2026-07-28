from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]
PYMUPDF4LLM = "pymupdf4llm"
OPTIONAL_TOOLS = ("codegraph", "pdftotext", "pandoc")


class InstallerTests(unittest.TestCase):
    def test_plugin_identity_and_skill_folder_are_wgo(self) -> None:
        manifest = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        self.assertEqual("wgo", manifest["name"])
        self.assertTrue((ROOT / "skills/wgo/SKILL.md").is_file())

    def test_claude_command_names_are_documented_as_slash_commands(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        installer = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("`/wgo_onboard`", readme)
        self.assertIn("`/wgo_operationalize`", readme)
        self.assertIn("In Claude, run /wgo_onboard", installer)

    def test_shell_installer_copies_wgo_and_installs_pymupdf4llm_after_consent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            target = temp_path / "target"
            bin_dir = temp_path / "bin"
            python_log = temp_path / "python.log"
            target.mkdir()
            bin_dir.mkdir()
            fake_python = bin_dir / "python3"
            fake_python.write_text(
                '#!/usr/bin/env sh\nprintf "%s\\n" "$*" >> "$PYTHON_LOG"\n'
                'if [ "$1" = "-c" ]; then exit 1; fi\n',
                encoding="utf-8",
            )
            fake_python.chmod(0o755)

            environment = os.environ | {
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "PYTHON_LOG": str(python_log),
            }
            result = subprocess.run(
                ["/bin/bash", str(ROOT / "install.sh"), str(target)],
                check=False,
                text=True,
                capture_output=True,
                env=environment,
                input="n\nn\nn\ny\n",
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertTrue((target / "plugins/wgo/skills/wgo/SKILL.md").is_file())
            self.assertTrue(
                (
                    target
                    / "plugins/wgo/skills/wgo/references/reviewers/architecture/reviewer.md"
                ).is_file()
            )
            self.assertTrue(
                (
                    target
                    / "plugins/wgo/skills/wgo/references/common/reviewer-contract.md"
                ).is_file()
            )
            self.assertTrue(
                (
                    target
                    / "plugins/wgo/skills/wgo/references/common/reviewer-authoring.md"
                ).is_file()
            )
            self.assertIn(f"-m pip install --user {PYMUPDF4LLM}", python_log.read_text(encoding="utf-8"))

    def test_shell_installer_skips_every_available_optional_tool(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            target = temp_path / "target"
            bin_dir = temp_path / "bin"
            target.mkdir()
            bin_dir.mkdir()
            extension = target / "plugins/wgo-reviewers/example"
            extension.mkdir(parents=True)
            marker = extension / "reviewer.md"
            marker.write_text("external reviewer\n", encoding="utf-8")

            for tool in (*OPTIONAL_TOOLS, "python3"):
                executable = bin_dir / tool
                executable.write_text("#!/usr/bin/env sh\nexit 0\n", encoding="utf-8")
                executable.chmod(0o755)

            result = subprocess.run(
                ["bash", str(ROOT / "install.sh"), str(target)],
                check=False,
                text=True,
                capture_output=True,
                env=os.environ | {"PATH": f"{bin_dir}:{os.environ['PATH']}"},
                input="",
            )

            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("external reviewer\n", marker.read_text(encoding="utf-8"))
            for name in ("CodeGraph", "pdftotext", "Pandoc", "PyMuPDF4LLM"):
                self.assertIn(f"{name} is already available.", result.stdout)
            self.assertNotIn("Install CodeGraph?", result.stdout)

    def test_windows_installer_has_the_same_optional_tool_contract(self) -> None:
        content = (ROOT / "install.bat").read_text(encoding="utf-8")
        for name in (
            "CodeGraph — code topology",
            "pdftotext — PDF discovery",
            "Pandoc — Office-document discovery",
            "PyMuPDF4LLM — enhanced PDF extraction (will install required Python distribution)",
        ):
            self.assertIn(name, content)
        self.assertIn("https://www.python.org/ftp/python/", content)
        self.assertIn("https://dl.xpdfreader.com/xpdf-tools-win-", content)
        self.assertIn("JohnMacFarlane.Pandoc", content)
        self.assertIn("colbymchenry/codegraph/main/install.ps1", content)
        self.assertIn(f'-m pip install --user "%PYMUPDF4LLM_PACKAGE%"', content)
        self.assertNotIn("astral.sh/uv", content)

    def test_shell_installer_checks_before_each_optional_install(self) -> None:
        content = (ROOT / "install.sh").read_text(encoding="utf-8")

        for executable in OPTIONAL_TOOLS:
            self.assertIn(f"command -v {executable}", content)
        self.assertIn("https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh", content)
        self.assertIn("https://dl.xpdfreader.com/xpdf-tools-mac-", content)
        self.assertIn("brew install pandoc", content)
        self.assertIn("PyMuPDF4LLM — enhanced PDF extraction (will install required Python distribution)", content)


if __name__ == "__main__":
    unittest.main()
