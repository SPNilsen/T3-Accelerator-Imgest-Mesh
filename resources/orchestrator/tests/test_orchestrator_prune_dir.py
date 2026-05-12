"""Targeted tests for _prune_dir in orchestrator router."""
import time
from pathlib import Path

from resources.orchestrator.app.router import _prune_dir


def _make_files(directory: Path, stems: list[str], suffix: str) -> None:
    """Create stub files with 0.01s gaps so mtime ordering is deterministic."""
    for stem in stems:
        f = directory / f"{stem}{suffix}"
        f.write_text("x", encoding="utf-8")
        time.sleep(0.01)


class TestPruneDirBasic:
    def test_25_files_leaves_20(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".bmp")

        _prune_dir(tmp_path, 20, [".bmp", ".txt"], [])

        remaining = list(tmp_path.glob("*.bmp"))
        assert len(remaining) == 20

    def test_exactly_20_files_nothing_deleted(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 21)]
        _make_files(tmp_path, stems, ".bmp")

        _prune_dir(tmp_path, 20, [".bmp", ".txt"], [])

        remaining = list(tmp_path.glob("*.bmp"))
        assert len(remaining) == 20


class TestPruneDirSidecars:
    def test_sidecar_meta_json_deleted_with_primary(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".bmp")
        for stem in stems:
            (tmp_path / f"{stem}.meta.json").write_text("{}", encoding="utf-8")

        _prune_dir(tmp_path, 20, [".bmp", ".txt"], [".meta.json"])

        for i in range(1, 6):
            assert not (tmp_path / f"frame-{i:05d}.bmp").exists()
            assert not (tmp_path / f"frame-{i:05d}.meta.json").exists()

        for i in range(6, 26):
            assert (tmp_path / f"frame-{i:05d}.bmp").exists()
            assert (tmp_path / f"frame-{i:05d}.meta.json").exists()

    def test_missing_sidecar_does_not_raise(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".bmp")

        # No sidecars created — must not raise
        _prune_dir(tmp_path, 20, [".bmp", ".txt"], [".meta.json"])

        remaining = list(tmp_path.glob("*.bmp"))
        assert len(remaining) == 20
