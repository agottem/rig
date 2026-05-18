import sys
import subprocess
import time


def print_acp_safe (text, **kwargs):
    print(text, file=sys.stderr, **kwargs)

def run_acp_safe (cmd, **kwargs):
    kwargs.setdefault("stdin", subprocess.DEVNULL)
    kwargs.setdefault("stdout", sys.stderr)
    return subprocess.run(cmd, **kwargs)

def wait_vm_ready (vm_name):
    while run_acp_safe(["incus", "exec", vm_name, "--", "true"]).returncode != 0:
        time.sleep(2)
