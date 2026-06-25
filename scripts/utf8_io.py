import os
import sys


def configure_utf8_stdio():
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")


def utf8_subprocess_env(env=None):
    subprocess_env = dict(os.environ if env is None else env)
    subprocess_env["PYTHONUTF8"] = "1"
    subprocess_env["PYTHONIOENCODING"] = "utf-8"
    return subprocess_env
