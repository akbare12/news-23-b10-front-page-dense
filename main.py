#!/usr/bin/env python3
"""news-image-20261123 entry: copies the pre-drawn entry.png to the output dir.

The grader runs this program with a read-only repository and a writable
output directory given by MAKEFUN_OUTPUT_DIR. Nothing is written next to
this file: the image is copied to <MAKEFUN_OUTPUT_DIR>/entry.png and the
copy is verified byte for byte before the program reports success.
"""
import hashlib
import os
import shutil
import sys


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_size(path):
    """Read width/height from a PNG IHDR chunk (stdlib only, no PIL)."""
    with open(path, "rb") as handle:
        head = handle.read(33)
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a PNG file")
    width = int.from_bytes(head[16:20], "big")
    height = int.from_bytes(head[20:24], "big")
    return width, height


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dst = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    src_hash = sha256_of(src)
    dst_hash = sha256_of(dst)
    if src_hash != dst_hash:
        print("FAIL: output hash %s != source hash %s" % (dst_hash, src_hash),
              file=sys.stderr)
        return 1
    width, height = png_size(dst)
    if (width, height) != (1024, 1024):
        print("FAIL: output is %dx%d, expected 1024x1024" % (width, height),
              file=sys.stderr)
        return 1
    print("OK entry.png %d bytes %dx%d sha256=%s"
          % (os.path.getsize(dst), width, height, dst_hash))
    return 0


if __name__ == "__main__":
    sys.exit(main())
