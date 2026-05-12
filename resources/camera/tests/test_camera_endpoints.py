"""Targeted tests for the /latest-thumb and /latest-frame camera endpoints."""
import shutil
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from resources.camera.app.status import app


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _client() -> TestClient:
    return TestClient(app, raise_server_exceptions=True)


# ---------------------------------------------------------------------------
# /latest-thumb
# ---------------------------------------------------------------------------

class TestLatestThumb:
    def test_returns_404_with_empty_output_dir(self, tmp_path: Path):
        empty_dir = tmp_path / "empty_output"
        empty_dir.mkdir()

        with patch("resources.camera.app.status._load_output_dir", return_value=empty_dir):
            client = _client()
            resp = client.get("/latest-thumb")

        assert resp.status_code == 404

    def test_returns_404_when_output_dir_does_not_exist(self, tmp_path: Path):
        missing_dir = tmp_path / "nonexistent"

        with patch("resources.camera.app.status._load_output_dir", return_value=missing_dir):
            client = _client()
            resp = client.get("/latest-thumb")

        assert resp.status_code == 404

    def test_returns_200_and_png_content_type_after_thumb_written(self, tmp_path: Path):
        out_dir = tmp_path / "output"
        out_dir.mkdir()
        thumb = out_dir / "frame-00001.thumb.png"
        # Minimal valid 1x1 PNG
        thumb.write_bytes(
            b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
            b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00"
            b"\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00\x05\x18"
            b"\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
        )

        with patch("resources.camera.app.status._load_output_dir", return_value=out_dir):
            client = _client()
            resp = client.get("/latest-thumb")

        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("image/png")

    def test_returns_most_recent_thumb(self, tmp_path: Path):
        import time

        out_dir = tmp_path / "output"
        out_dir.mkdir()
        older = out_dir / "frame-00001.thumb.png"
        older.write_bytes(b"OLD")
        time.sleep(0.02)
        newer = out_dir / "frame-00002.thumb.png"
        newer.write_bytes(b"NEW")

        with patch("resources.camera.app.status._load_output_dir", return_value=out_dir):
            client = _client()
            resp = client.get("/latest-thumb")

        # Should serve the newer file — content is "NEW"
        assert resp.status_code == 200
        assert resp.content == b"NEW"


# ---------------------------------------------------------------------------
# /latest-frame
# ---------------------------------------------------------------------------

class TestLatestFrame:
    def test_returns_404_with_empty_output_dir(self, tmp_path: Path):
        empty_dir = tmp_path / "empty_output"
        empty_dir.mkdir()

        with patch("resources.camera.app.status._load_output_dir", return_value=empty_dir):
            client = _client()
            resp = client.get("/latest-frame")

        assert resp.status_code == 404

    def test_returns_404_when_output_dir_does_not_exist(self, tmp_path: Path):
        missing_dir = tmp_path / "nonexistent"

        with patch("resources.camera.app.status._load_output_dir", return_value=missing_dir):
            client = _client()
            resp = client.get("/latest-frame")

        assert resp.status_code == 404

    def test_returns_200_and_bmp_content_type_after_bmp_written(self, tmp_path: Path):
        out_dir = tmp_path / "output"
        out_dir.mkdir()
        bmp = out_dir / "frame-00001.bmp"
        # Minimal BMP header (54 bytes) for a 1x1 24bpp image
        bmp.write_bytes(
            b"BM" + b"\x00" * 52  # simplified stub — enough for the file to exist
        )

        with patch("resources.camera.app.status._load_output_dir", return_value=out_dir):
            client = _client()
            resp = client.get("/latest-frame")

        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("image/bmp")

    def test_returns_most_recent_bmp(self, tmp_path: Path):
        import time

        out_dir = tmp_path / "output"
        out_dir.mkdir()
        older = out_dir / "frame-00001.bmp"
        older.write_bytes(b"OLD")
        time.sleep(0.02)
        newer = out_dir / "frame-00002.bmp"
        newer.write_bytes(b"NEW")

        with patch("resources.camera.app.status._load_output_dir", return_value=out_dir):
            client = _client()
            resp = client.get("/latest-frame")

        assert resp.status_code == 200
        assert resp.content == b"NEW"


# ---------------------------------------------------------------------------
# Emitter thumbnail copy integration
# ---------------------------------------------------------------------------

class TestEmitterThumbCopy:
    def test_emit_bmp_frame_copies_thumb_when_present(self, tmp_path: Path):
        """emit_bmp_frame should copy the paired .thumb.png to output dir."""
        import shutil

        from resources.camera.app.emitter import emit_bmp_frame

        # Create a minimal sample BMP in a fake input dir
        input_dir = tmp_path / "input"
        input_dir.mkdir()
        bmp = input_dir / "sample.bmp"
        # Valid minimal 2x2 BMP (header + pixel data)
        bmp.write_bytes(b"BM" + b"\x00" * 52)

        # Create the paired thumbnail
        thumb_src = input_dir / "sample.thumb.png"
        thumb_src.write_bytes(b"THUMB")

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        emit_bmp_frame(output_dir, input_dir, "frame", 1, max_frames=20)

        # Output dir should contain exactly one .thumb.png
        thumbs = list(output_dir.glob("*.thumb.png"))
        assert len(thumbs) == 1
        assert thumbs[0].read_bytes() == b"THUMB"

    def test_emit_bmp_frame_continues_without_thumb(self, tmp_path: Path):
        """emit_bmp_frame should not raise when no thumb exists for the BMP."""
        from resources.camera.app.emitter import emit_bmp_frame

        input_dir = tmp_path / "input"
        input_dir.mkdir()
        bmp = input_dir / "sample.bmp"
        bmp.write_bytes(b"BM" + b"\x00" * 52)
        # Deliberately NOT creating a .thumb.png

        output_dir = tmp_path / "output"
        output_dir.mkdir()

        # Must not raise
        emit_bmp_frame(output_dir, input_dir, "frame", 1, max_frames=20)

        thumbs = list(output_dir.glob("*.thumb.png"))
        assert len(thumbs) == 0
