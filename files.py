import subprocess
import sys
import tempfile
from pathlib import Path


def format_path(path):
    path = str(path)
    if sys.platform.startswith('win32'):
        return path.replace('\\', '/')
    else:
        return path


def run_file(path, kill_time=None):
    path = format_path(path)
    if sys.platform.startswith('win32'):
        sub_p = subprocess.run(path, stdout=subprocess.PIPE,
                               shell=True, timeout=kill_time)
    else:
        sub_p = subprocess.run(
            ['sh', path], stdout=subprocess.PIPE, timeout=kill_time)
    return sub_p.stdout.decode('utf-8')


def run_command(cmd, kill_time=None):
    return subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, timeout=kill_time).stdout.decode('utf-8') + '\n'


def run_commands(cmd_payload, kill_time=None):
    tmp_file = Path(tempfile.NamedTemporaryFile().name)
    tmp_file.write_text(cmd_payload)
    output = run_file(tmp_file, kill_time)
    if tmp_file.exists():
        tmp_file.unlink()
    return output
