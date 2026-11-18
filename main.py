"""News image for 18 November 2026 — make.fun bounty entry.

Copies the pre-rendered entry image (entry.png, in this repository) to the
output directory as entry.png, byte-for-byte.

Standard library only. Deterministic: no network, no randomness, no clock.
The output is always an exact copy of the bundled entry.png.

Usage:
    python3 main.py

Output directory: $MAKEFUN_OUTPUT_DIR if set, otherwise ./output
(relative to the current working directory).
"""

import hashlib
import os
import shutil
import sys

SOURCE_FILENAME = "entry.png"


def resolve_paths(argv):
    """Return (source_path, output_dir, output_path)."""
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, SOURCE_FILENAME)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or os.path.join(
        os.getcwd(), "output"
    )
    output = os.path.join(output_dir, SOURCE_FILENAME)
    return source, output_dir, output


def copy_entry(source, output_dir, output):
    """Copy entry.png byte-for-byte into the output directory.

    Verifies the copy afterwards: the output must be byte-identical to the
    bundled source, otherwise the run fails instead of silently shipping a
    truncated or corrupted image.
    """
    if not os.path.isfile(source):
        raise FileNotFoundError("bundled image not found: %s" % source)
    os.makedirs(output_dir, exist_ok=True)
    shutil.copyfile(source, output)
    if sha256_of(source) != sha256_of(output):
        raise RuntimeError("copy verification failed: %s != %s" % (source, output))
    return output


def sha256_of(path):
    """Return the hex SHA-256 digest of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv):
    source, output_dir, output = resolve_paths(argv)
    copy_entry(source, output_dir, output)
    print("wrote %s" % output)
    print("sha256 %s" % sha256_of(output))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
