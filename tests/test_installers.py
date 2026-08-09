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
    def test_provider_manifests_share_the_wgo_identity_and_core_version(self) -> None:
        codex_manifest = json.loads(
            (ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8")
        )
        claude_manifest = json.loads(
            (ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8")
        )
        self.assertEqual("wgo", codex_manifest["name"])
        self.assertEqual("wgo", claude_manifest["name"])
        self.assertEqual(
            codex_manifest["version"].split("+", maxsplit=1)[0],
            claude_manifest["version"].split("+", maxsplit=1)[0],
        )
        self.assertTrue((ROOT / "skills/wgo/SKILL.md").is_file())

    def test_provider_command_names_are_documented(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        onboarding_docs = (ROOT / "docs/onboarding-expectations.md").read_text(
            encoding="utf-8"
        )
        installer = (ROOT / "install.sh").read_text(encoding="utf-8")
        self.assertIn("`/wgo:onboard`", readme)
        self.assertIn("`/wgo:operationalize`", readme)
        self.assertIn("`/wgo-onboard`", readme)
        self.assertIn("`/wgo-operationalize`", readme)
        self.assertIn("In Claude, run /wgo:onboard", installer)
        self.assertIn("In OpenCode, run /wgo-onboard", installer)
        for command in (
            "/wgo:onboard compare [YYYYMMDD]",
            "/wgo:onboard blind-compare [YYYYMMDD]",
            "/wgo-onboard compare [YYYYMMDD]",
            "/wgo-onboard blind-compare [YYYYMMDD]",
            "/wgo-audit all",
        ):
            self.assertIn(command, onboarding_docs)
        self.assertNotIn("/wgo_onboard", onboarding_docs)

    def test_canonical_frontmatter_contains_both_provider_contracts(self) -> None:
        skill = (ROOT / "skills/wgo/SKILL.md").read_text(encoding="utf-8")
        onboard = (ROOT / "commands/onboard.md").read_text(encoding="utf-8")

        self.assertIn("when_to_use:", skill)
        self.assertIn("user-invocable: false", skill)
        self.assertIn('args: "[compare|blind-compare] [YYYYMMDD]"', onboard)
        self.assertIn("skills: wgo", onboard)
        self.assertIn('argument-hint: "[compare|blind-compare] [YYYYMMDD]"', onboard)
        self.assertIn("disable-model-invocation: true", onboard)

    def test_shell_installer_copies_wgo_and_installs_pymupdf4llm_after_consent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            temp_path = Path(temp)
            target = temp_path / "target"
            bin_dir = temp_path / "bin"
            python_log = temp_path / "python.log"
            target.mkdir()
            bin_dir.mkdir()
            legacy_command = target / ".claude/commands/wgo_onboard.md"
            legacy_command.parent.mkdir(parents=True)
            legacy_command.write_text("legacy command\n", encoding="utf-8")
            legacy_skill = target / ".claude/skills/wgo/SKILL.md"
            legacy_skill.parent.mkdir(parents=True)
            legacy_skill.write_text("legacy skill\n", encoding="utf-8")
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
            codex_skill = (target / "plugins/wgo/skills/wgo/SKILL.md").read_text(
                encoding="utf-8"
            )
            codex_onboard = (target / "plugins/wgo/commands/onboard.md").read_text(
                encoding="utf-8"
            )
            self.assertNotIn("when_to_use:", codex_skill)
            self.assertNotIn("user-invocable:", codex_skill)
            self.assertIn("args:", codex_onboard)
            self.assertIn("skills:", codex_onboard)
            self.assertNotIn("argument-hint:", codex_onboard)
            self.assertNotIn("disable-model-invocation:", codex_onboard)
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
            self.assertTrue(
                (
                    target
                    / "plugins/wgo/skills/wgo/references/common/cost-estimation-claude.md"
                ).is_file()
            )
            self.assertTrue(
                (
                    target
                    / "plugins/wgo/skills/wgo/references/common/cost-estimation-opencode.md"
                ).is_file()
            )
            claude_plugin = target / ".claude/skills/wgo-claude"
            self.assertTrue((claude_plugin / ".claude-plugin/plugin.json").is_file())
            self.assertTrue((claude_plugin / "SKILL.md").is_file())
            self.assertTrue((claude_plugin / "commands/onboard.md").is_file())
            self.assertTrue(
                (claude_plugin / "references/common/reviewer-contract.md").is_file()
            )
            self.assertTrue(
                (claude_plugin / "references/common/cost-estimation-claude.md").is_file()
            )
            claude_skill = (claude_plugin / "SKILL.md").read_text(encoding="utf-8")
            claude_onboard = (claude_plugin / "commands/onboard.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("when_to_use:", claude_skill)
            self.assertIn("user-invocable: false", claude_skill)
            self.assertNotIn("args:", claude_onboard)
            self.assertNotIn("skills:", claude_onboard)
            self.assertIn("argument-hint:", claude_onboard)
            self.assertIn("disable-model-invocation: true", claude_onboard)
            opencode_onboard_path = target / ".opencode/commands/wgo-onboard.md"
            self.assertTrue(opencode_onboard_path.is_file())
            opencode_onboard = opencode_onboard_path.read_text(encoding="utf-8")
            self.assertIn("description:", opencode_onboard)
            self.assertNotIn("\nname:", opencode_onboard)
            self.assertNotIn("\nargs:", opencode_onboard)
            self.assertNotIn("\nskills:", opencode_onboard)
            self.assertNotIn("\nargument-hint:", opencode_onboard)
            self.assertNotIn("\ndisable-model-invocation:", opencode_onboard)
            self.assertIn("OpenCode command arguments: `$ARGUMENTS`.", opencode_onboard)
            self.assertIn("read `.opencode/skills/wgo/SKILL.md` directly", opencode_onboard)
            self.assertIn("Load and use the WGO skill.", opencode_onboard)
            opencode_skill_path = target / ".opencode/skills/wgo/SKILL.md"
            self.assertTrue(opencode_skill_path.is_file())
            opencode_skill = opencode_skill_path.read_text(encoding="utf-8")
            self.assertIn("\nname: wgo", opencode_skill)
            self.assertIn("\ndescription:", opencode_skill)
            self.assertNotIn("\nwhen_to_use:", opencode_skill)
            self.assertNotIn("\nuser-invocable:", opencode_skill)
            self.assertTrue(
                (target / ".opencode/skills/wgo/references/common/reviewer-contract.md").is_file()
            )
            self.assertTrue(
                (
                    target
                    / ".opencode/skills/wgo/references/common/cost-estimation-opencode.md"
                ).is_file()
            )
            self.assertFalse(legacy_command.exists())
            self.assertFalse(legacy_skill.exists())
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
        self.assertIn("scripts\\filter-frontmatter.ps1", content)
        self.assertIn(".claude-plugin\\plugin.json", content)
        self.assertIn("/wgo:onboard", content)
        self.assertIn(".opencode\\commands", content)
        self.assertIn("/wgo-onboard", content)
        self.assertIn("opencode", (ROOT / "scripts/filter-frontmatter.ps1").read_text(encoding="utf-8"))
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
