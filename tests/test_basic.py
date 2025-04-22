import pytest
import enum
import sys
from snaparg import SnapArgumentParser
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
    import builtins
    from io import StringIO
    from contextlib import redirect_stdout

    # Simulate command-line input
    test_args = ["progname", "--moed", "FAST"]
    monkeypatch.setattr(sys, "argv", test_args)

    output = StringIO()
    with redirect_stdout(output):  # Redirect all print to `output`
        class Mode(enum.Enum):
            FAST = "FAST"
            SLOW = "SLOW"
            MEDIUM = "MEDIUM"

        parser = SnapArgumentParser()
        parser.add_argument("--mode", type=Mode)
        parser.add_argument("--count", type=int)

        try:
            parser.parse_args()
        except SystemExit:
            pass  # Expected exit on error

    output_value = output.getvalue()
    assert "Did you mean" in output_value, "No suggestion given in error message"
    assert "--mode" in output_value, "'--mode' not suggested"



def test_help_coloring(monkeypatch):
    parser = SnapArgumentParser()
    parser.add_argument("--mode", type=Mode)
    parser.add_argument("filename", help="Input file")

    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()

    help_output = f.getvalue()
    assert "\033[96mOptional arguments:\033[0m" in help_output  # ANSI cyan

