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

def test_invalid_flag_suggestion():
    import subprocess
    import tempfile
    import sys
    from pathlib import Path

    # Script to be tested
    test_script = """
import sys
import enum
from snaparg import SnapArgumentParser

class Mode(enum.Enum):
    FAST = "FAST"
    SLOW = "SLOW"
    MEDIUM = "MEDIUM"

parser = SnapArgumentParser()
parser.add_argument("--mode", type=Mode)
parser.add_argument("--count", type=int)

parser.parse_args()
"""

    # Write to a temporary file
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir) / "temp_snaparg_test.py"
        temp_path.write_text(test_script)

        # Run the script with an invalid flag
        result = subprocess.run(
            [sys.executable, str(temp_path), "--mod", "FAST"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
    print("=== STDOUT ===")
    print(result.stdout)
    print("=== RETURN CODE ===")
    print(result.returncode)

    # Assertions with better failure messages
    assert result.returncode != 0, f"Expected non-zero exit code, got {result.returncode}"
    assert "Did you mean" in result.stdout, f"'Did you mean' not found in output:\n{result.stdout}"
    assert "--mod" in result.stdout, f"'--mod' not found in output:\n{result.stdout}"
    assert "--mode" in result.stdout, f"'--mode' not suggested in output:\n{result.stdout}"

def test_help_coloring(monkeypatch):
    parser = SnapArgumentParser()
    parser.add_argument("--mode", type=Mode)
    parser.add_argument("filename", help="Input file")

    f = StringIO()
    with redirect_stdout(f):
        parser.print_help()

    help_output = f.getvalue()
    assert "\033[96mOptional arguments:\033[0m" in help_output  # ANSI cyan

