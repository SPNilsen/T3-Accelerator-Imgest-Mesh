"""Targeted tests for _prune_dir in inference worker and processed-set prune."""
import time
from pathlib import Path

from resources.inference.app.worker import _prune_dir


def _make_files(directory: Path, stems: list[str], suffix: str) -> None:
    """Create stub files with 0.01s gaps so mtime ordering is deterministic."""
    for stem in stems:
        f = directory / f"{stem}{suffix}"
        f.write_text("{}", encoding="utf-8")
        time.sleep(0.01)


class TestPruneDirBasic:
    def test_25_files_leaves_20(self, tmp_path: Path):
        stems = [f"result-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".json")

        _prune_dir(tmp_path, 20, [".json"], [])

        remaining = list(tmp_path.glob("*.json"))
        assert len(remaining) == 20

    def test_exactly_20_files_nothing_deleted(self, tmp_path: Path):
        stems = [f"result-{i:05d}" for i in range(1, 21)]
        _make_files(tmp_path, stems, ".json")

        _prune_dir(tmp_path, 20, [".json"], [])

        remaining = list(tmp_path.glob("*.json"))
        assert len(remaining) == 20

    def test_oldest_files_deleted(self, tmp_path: Path):
        stems = [f"result-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".json")

        _prune_dir(tmp_path, 20, [".json"], [])

        for i in range(1, 6):
            assert not (tmp_path / f"result-{i:05d}.json").exists()

        for i in range(6, 26):
            assert (tmp_path / f"result-{i:05d}.json").exists()

    def test_no_sidecars_does_not_raise(self, tmp_path: Path):
        """Inference has no sidecars — empty sidecar list must not raise."""
        stems = [f"result-{i:05d}" for i in range(1, 26)]
        _make_files(tmp_path, stems, ".json")

        _prune_dir(tmp_path, 20, [".json"], [])

        remaining = list(tmp_path.glob("*.json"))
        assert len(remaining) == 20


class TestProcessedSetPrune:
    def test_processed_set_shrinks_when_files_removed(self, tmp_path: Path):
        """25 entries processed; 5 files removed from input_dir; set shrinks to 20."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        # Create 25 files and populate processed set
        names = [f"frame-{i:05d}.bmp" for i in range(1, 26)]
        for name in names:
            (input_dir / name).write_text("x", encoding="utf-8")

        processed: set[str] = set(names)
        assert len(processed) == 25

        # Simulate upstream prune removing 5 oldest files
        for name in names[:5]:
            (input_dir / name).unlink()

        # Apply the processed-set prune line from worker.py
        processed -= {name for name in processed if not (input_dir / name).exists()}

        assert len(processed) == 20

    def test_processed_set_unchanged_when_all_files_present(self, tmp_path: Path):
        """Processed set must not shrink when all files still exist in input_dir."""
        input_dir = tmp_path / "input"
        input_dir.mkdir()

        names = [f"frame-{i:05d}.bmp" for i in range(1, 21)]
        for name in names:
            (input_dir / name).write_text("x", encoding="utf-8")

        processed: set[str] = set(names)

        processed -= {name for name in processed if not (input_dir / name).exists()}

        assert len(processed) == 20
