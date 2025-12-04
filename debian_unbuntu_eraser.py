#!/usr/bin/env python3
import os
import glob
import sys
import stat
import logging
from datetime import datetime
logging.basicConfig(filename='/dev/null', level=logging.ERROR)
SAFE_LOGS_DEBIAN = [
    # Users command history
    '/home/*/.bash_history',
    '/home/*/.zsh_history',
    '/root/.bash_history',
    '/root/.zsh_history',
    '/home/*/.mysql_history',
    '/home/*/.python_history',
    '/root/.mysql_history',
    '/root/.python_history',
    # Connection logs
    '/var/log/auth.log*',
    '/var/log/wtmp',
    '/var/log/btmp',
    '/var/log/lastlog',
    '/var/log/faillog',
    # System logs
    '/var/log/syslog*',
    '/var/log/kern.log*',
    '/var/log/dmesg',
    # apt/sudo logs
    '/var/log/sudo.log',
    '/var/log/apt/history.log',
    '/var/log/apt/term.log',
]

def safe_clear(filepath):
    try:
        if not os.path.isfile(filepath):
            return False
        if not any(filepath.startswith(p) for p in ['/home/', '/var/log/', '/root/']):
            return False
        st = os.stat(filepath)
        uid, gid = st.st_uid, st.st_gid
        mode = stat.S_IMODE(st.st_mode)
        with open(filepath, 'w') as f:
            f.write('')
        os.chown(filepath, uid, gid)
        os.chmod(filepath, mode)
        return True
    except Exception:
        return False

def main():
    print(f"[DEBIAN/UBUNTU] Starting SAFE log cleanup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for pattern in SAFE_LOGS_DEBIAN:
        for filepath in glob.glob(pattern):
            if safe_clear(filepath):
                print(f"[+] OK: {filepath}")
            else:
                print(f"[!] Failed: {filepath} (invalid path or permission)")
    print("[DEBIAN/UBUNTU] Cleanup completed.")

if __name__ == "__main__":
    main()
