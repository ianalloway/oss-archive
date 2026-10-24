"""Run the status generator against disposable, local Git repositories."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate-status.sh"


class StatusGeneratorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.remote = root / "archive.git"
        self.source = root / "source"
        self.work = root / "work"
        self.git("init", "--bare", str(self.remote))
        self.git("init", str(self.source))
        self.git("-C", str(self.source), "config", "user.name", "Fixture")
        self.git("-C", str(self.source), "config", "user.email", "fixture@example.test")
        for season, timestamp in (("winter", "2026-01-01T12:00:00+00:00"),
                                  ("summer", "2026-07-01T12:00:00+00:00")):
            (self.source / "fixture.txt").write_text(season, encoding="utf-8")
            self.git("-C", str(self.source), "add", "fixture.txt")
            env = {**os.environ, "GIT_AUTHOR_DATE": timestamp, "GIT_COMMITTER_DATE": timestamp}
            self.git("-C", str(self.source), "commit", "-m", f"Snapshot {season}", env=env)
            self.git("-C", str(self.source), "push", str(self.remote),
                     f"HEAD:refs/heads/archive/{season}")
        self.git("init", str(self.work))
        self.git("-C", str(self.work), "remote", "add", "origin", str(self.remote))
        (self.work / "scripts").mkdir()
        self.script = self.work / "scripts" / SCRIPT.name
        shutil.copy2(SCRIPT, self.script)
        self.output = self.work / "STATUS.md"
        self.output.write_text("Previous status\n", encoding="utf-8")

    def git(self, *args, env=None):
        return subprocess.run(["git", *args], env=env, capture_output=True,
                              text=True, check=True).stdout

    def generate(self, *, no_mapfile=False, env=None):
        command = ["bash", str(self.script)]
        if no_mapfile:
            command = ["bash", "-c", 'enable -n mapfile 2>/dev/null || true; source "$0"',
                       str(self.script)]
        return subprocess.run(command, env=env, capture_output=True, text=True, timeout=15)

    def test_works_without_the_bash_four_mapfile_builtin(self):
        before = self.git("--git-dir", str(self.remote), "show-ref")
        result = self.generate(no_mapfile=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("**Branches:** 2", self.output.read_text())
        self.assertEqual(self.git("--git-dir", str(self.remote), "show-ref"), before)

    def test_dates_are_new_york_time_without_gnu_date(self):
        bin_dir = self.work / "bin"
        bin_dir.mkdir()
        fake_date = bin_dir / "date"
        fake_date.write_text(
            '#!/usr/bin/env bash\nif [[ "$1" == "-d" ]]; then exit 1; fi\n'
            f'exec "{shutil.which("date")}" "$@"\n', encoding="utf-8"
        )
        fake_date.chmod(0o755)
        env = {**os.environ, "TZ": "Asia/Tokyo", "PATH": f'{bin_dir}:{os.environ["PATH"]}'}
        result = self.generate(env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = self.output.read_text()
        self.assertIn("2026-01-01 07:00 EST", output)
        self.assertIn("2026-07-01 08:00 EDT", output)
        self.assertIn("git remote rename origin archive", output)

    def test_failed_fetch_keeps_existing_status(self):
        self.git("-C", str(self.work), "remote", "set-url", "origin", str(self.work / "missing"))
        self.assertNotEqual(self.generate().returncode, 0)
        self.assertEqual(self.output.read_text(), "Previous status\n")

    def test_empty_archive_keeps_existing_status(self):
        empty = self.work / "empty.git"
        self.git("init", "--bare", str(empty))
        self.git("-C", str(self.work), "remote", "set-url", "origin", str(empty))
        self.assertNotEqual(self.generate().returncode, 0)
        self.assertEqual(self.output.read_text(), "Previous status\n")


if __name__ == "__main__":
    unittest.main()
