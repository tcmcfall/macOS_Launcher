# -*- coding: utf-8 -*-
import subprocess
import shlex
from typing import List, Optional, Tuple
from .log import info, warn, error

def run(cmd: List[str], timeout: Optional[int]=None) -> Tuple[int, str, str]:
    try:
        info("exec: " + " ".join(shlex.quote(c) for c in cmd))
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
        if p.returncode != 0:
            warn(f"command rc={p.returncode}: {p.stderr.strip()}")
        return p.returncode, (p.stdout or ""), (p.stderr or "")
    except subprocess.TimeoutExpired as te:
        error(f"timeout running: {' '.join(cmd)}")
        return 124, "", str(te)
    except Exception as e:
        error(f"exception running: {' '.join(cmd)} :: {e}")
        return 1, "", str(e)

def hide_kodi() -> None:
    run(["/usr/bin/osascript", "-e", 'tell application "Kodi" to hide'])

def activate_kodi() -> None:
    run(["/usr/bin/osascript", "-e", 'tell application "Kodi" to activate'])

def open_app_wait(app_path: str) -> bool:
    rc, _, _ = run(["/usr/bin/open", "-W", app_path])
    return rc == 0
