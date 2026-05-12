"""Targeted tests for _prune_dir in camera emitter and emit_frame integration."""
import time
from pathlib import Path

import pytest

from resources.camera.app.emitter import _prune_dir, emit_placeholder_frame


# ---------------------------------------------------------------------------
# _prune_dir unit tests
# ---------------------------------------------------------------------------


def _make_files(directory: Path, stems: list[str], suffix: str) -> None:
    """Create stub files with 0.01s gaps so mtime ordering is deterministic."""
    for stem in stems:
        f = directory / f"{stem}{suffix}"
        f.write_text("x", encoding="utf-8")
        time.sleep(0.01)


class TestPruneDirBasic:
    def test_25_files_leaves_20(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".txt")

        _prune_dir(tmp_path, 20, [".txt"], [])

        remaining = list(tmp_path.glob("*.txt"))
        assert len(remaining) == 20

    def test_exactly_20_files_nothing_deleted(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 21)]
        _make_files(tmp_path, stems, ".txt")

        _prune_dir(tmp_path, 20, [".txt"], [])

        remaining = list(tmp_path.glob("*.txt"))
        assert len(remaining) == 20

    def test_oldest_files_deleted(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".txt")

        _prune_dir(tmp_path, 20, [".txt"], [])

        # Oldest 5 (frame-00001 through frame-00005) must be gone
        for i in range(1, 6):
            assert not (tmp_path / f"frame-{i:05d}.txt").exists()

        # Newest 20 must remain
        for i in range(6, 26):
            assert (tmp_path / f"frame-{i:05d}.txt").exists()


class TestPruneDirSidecars:
    def test_sidecar_meta_json_deleted_with_primary(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".bmp")
        # Create meta.json sidecars for all
        for stem in stems:
            (tmp_path / f"{stem}.meta.json").write_text("{}", encoding="utf-8")

        _prune_dir(tmp_path, 20, [".bmp"], [".meta.json"])

        # Oldest 5 primary and sidecars must be gone
        for i in range(1, 6):
            assert not (tmp_path / f"frame-{i:05d}.bmp").exists()
            assert not (tmp_path / f"frame-{i:05d}.meta.json").exists()

        # Newest 20 primaries and sidecars must remain
        for i in range(6, 26):
            assert (tmp_path / f"frame-{i:05d}.bmp").exists()
            assert (tmp_path / f"frame-{i:05d}.meta.json").exists()

    def test_thumb_png_sidecar_deleted_with_primary(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".bmp")
        for stem in stems:
            (tmp_path / f"{stem}.meta.json").write_text("{}", encoding="utf-8")
            (tmp_path / f"{stem}.thumb.png").write_bytes(b"\x89PNG")

        _prune_dir(tmp_path, 20, [".bmp"], [".meta.json", ".thumb.png"])

        for i in range(1, 6):
            assert not (tmp_path / f"frame-{i:05d}.thumb.png").exists()

    def test_missing_sidecar_does_not_raise(self, tmp_path: Path):
        stems = [f"frame-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".bmp")
        # Deliberately do NOT create any .meta.json sidecars

        # Must not raise even though sidecars are absent
        _prune_dir(tmp_path, 20, [".bmp"], [".meta.json", ".thumb.png"])

        remaining = list(tmp_path.glob("*.bmp"))
        assert len(remaining) == 20


# ---------------------------------------------------------------------------
# emit_placeholder_frame integration smoke test
# ---------------------------------------------------------------------------


class TestEmitPlaceholderIntegration:
    def test_25_emits_leaves_at_most_20_primaries(self, tmp_path: Path):
        for i in range(1, 26):
            emit_placeholder_frame(str(tmp_path), "frame", i, max_frames=20)

        primaries = list(tmp_path.glob("*.txt"))
        assert len(primaries) <= 20
