#!/usr/bin/env python3
"""Entrypoint for the make.fun news-image-20261122-36 entry.

Reads entry.png next to this file and copies it into the directory
named by MAKEFUN_OUTPUT_DIR (default /output). Standard library only,
so it runs in the grader's pinned python3.13 image with no network
and no extra packages.
"""

import os
import struct
import sys
import zlib
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_SIZE = 1_048_576


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_png(data: bytes) -> None:
    """Check the PNG signature, every chunk CRC, IHDR size and total size."""
    if len(data) < 8 or data[:8] != PNG_SIGNATURE:
        fail("not a PNG file (bad 8-byte signature)")
    if len(data) >= MAX_SIZE:
        fail(f"file too large: {len(data)} bytes (limit {MAX_SIZE})")
    offset = 8
    saw_ihdr = False
    while offset < len(data):
        if offset + 8 > len(data):
            fail("truncated chunk header")
        length = struct.unpack(">I", data[offset:offset + 4])[0]
        chunk_type = data[offset + 4:offset + 8]
        chunk_end = offset + 8 + length + 4
        if chunk_end > len(data):
            fail(f"truncated chunk {chunk_type!r}")
        stored_crc = struct.unpack(">I", data[chunk_end - 4:chunk_end])[0]
        actual_crc = zlib.crc32(chunk_type)
        actual_crc = zlib.crc32(data[offset + 8:offset + 8 + length], actual_crc)
        if actual_crc != stored_crc:
            fail(f"bad CRC in chunk {chunk_type!r}")
        if chunk_type == b"IHDR":
            if length != 13:
                fail("IHDR chunk has wrong length")
            width, height = struct.unpack(">II", data[offset + 8:offset + 16])
            if (width, height) != (1024, 1024):
                fail(f"wrong size: {width}x{height} (expected 1024x1024)")
            saw_ihdr = True
        offset = chunk_end
    if not saw_ihdr:
        fail("missing IHDR chunk")


def main() -> int:
    source = Path(__file__).resolve().parent / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    data = source.read_bytes()
    validate_png(data)
    dest = out_dir / "entry.png"
    dest.write_bytes(data)
    print(f"wrote {dest} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
