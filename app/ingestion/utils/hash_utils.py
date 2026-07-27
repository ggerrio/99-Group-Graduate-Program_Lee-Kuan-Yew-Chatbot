import hashlib
from pathlib import Path

def compute_file_sha256(file_path: Path) -> str:
    """
    Computes the SHA256 hex digest of a file for change tracking.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            sha256.update(chunk)
    return sha256.hexdigest()
