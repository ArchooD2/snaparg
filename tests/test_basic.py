import pytest
import enum
import sys
from snaparg import SnapArgumentParser  # Adjust this import path to your file structure
from io import StringIO
from contextlib import redirect_stdout, redirect_stderr

class Mode(enum.Enum):
    FAST = enum.auto()
    SLOW = enum.auto()
    MEDIUM = enum.auto()

def test_valid_enum_parsing():
    parser = SnapArgumentParser()
    parser.add_argument("--mode", type=Mode)
    args = parser.parse_args(["--mode", "FAST"])
    assert args.mode == Mode.FAST  # not 1

def test_invalid_flag_suggestion(monkeypatch):
    parser = SnapArgumentParser()
    parser.add_argument("--mode", type=Mode)
    parser.add_argument("--count", type=int)

    fake_argv = ["script.py", "--mod", "FAST"]
    monkeypatch.setattr(sys, "argv", fake_argv)

    f = StringIO()
    with redirect_stdout(f), redirect_stderr(f):
        with pytest.raises(SystemExit):
            parser.parse_args()


    output = f.getvalue()
    assert "Did you mean" in output
    assert "--mod" in output
    assert "--mode" in output

def test_help_coloring(monkeypatch):
    parser = SnapArgumentParser()
    parser.add_argument("--mode", type=Mode)
    parser.add_argument("filename", help="Input file")

    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()

    help_output = f.getvalue()
    assert "\033[96mOptional arguments:\033[0m" in help_output  # ANSI cyan

