"""Locate the film folder the toolkit works on: $FILM if set, else the current directory.
Every toolkit command runs from inside a film folder (the one holding script.json)."""
import os, pathlib, sys

def film_dir():
    d = pathlib.Path(os.environ.get("FILM") or os.getcwd()).resolve()
    if not (d / "script.json").exists():
        sys.exit(f"not a film folder (no script.json): {d}\nRun from films/<source-repo>/<film>/ or set FILM=<path>.")
    return d
