"""Keep this installed skill aligned with Ivor-NCUT/fanhan-design via gh api."""

import base64
import hashlib
import json
import os
import shutil
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = "repos/Ivor-NCUT/fanhan-design"


def api(path):
    env = {**os.environ, "GODEBUG": "http2client=0"}
    for attempt in range(3):
        try:
            endpoint = f"{REPO}/{path}" if path else REPO
            return json.loads(subprocess.check_output(["gh", "api", endpoint], text=True, env=env))
        except subprocess.CalledProcessError:
            if attempt == 2:
                raise
            time.sleep(2)


def blob_hash(data):
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def main():
    branch = api("")["default_branch"]
    commit = api(f"commits/{branch}")["sha"]
    tree = api(f"git/trees/{commit}?recursive=1")
    if tree.get("truncated"):
        raise RuntimeError("GitHub file list was truncated; local skill was not changed")
    files = {item["path"]: item for item in tree["tree"] if item["type"] == "blob"}
    changed = []
    for name, item in files.items():
        target = (ROOT / name).resolve()
        if not target.is_relative_to(ROOT) or item["mode"] not in ("100644", "100755"):
            raise RuntimeError(f"Unsafe GitHub path or mode: {name}")
        if not target.is_file() or blob_hash(target.read_bytes()) != item["sha"]:
            changed.append((name, item, target))
    if not changed:
        print(f"fanhan-design matches {commit[:12]}")
        return

    # Fetch and verify everything before touching the installed skill.
    updates = []
    for name, item, target in changed:
        payload = api(f"git/blobs/{item['sha']}")
        if payload.get("encoding") != "base64":
            raise RuntimeError(f"Unsupported blob encoding: {name}")
        data = base64.b64decode(payload["content"])
        if blob_hash(data) != item["sha"]:
            raise RuntimeError(f"GitHub blob checksum mismatch: {name}")
        updates.append((name, item, target, data))

    backup = ROOT / ".sync-backups" / datetime.now().strftime("%Y%m%d-%H%M%S")
    for name, item, target, data in updates:
        if target.exists():
            saved = backup / name
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        target.chmod(0o755 if item["mode"] == "100755" else 0o644)
    print(f"Updated {len(updates)} files to {commit[:12]}; prior files: {backup}")


if __name__ == "__main__":
    main()
