import argparse
import sys
import difflib
import enum
import textwrap
from functools import partial

# ANSI colors
BOLD = "\033[1m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"


class SnapArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        if sys.version_info > (3, 11):
            kwargs.setdefault("exit_on_error", True)
        kwargs.setdefault("formatter_class", partial(argparse.HelpFormatter, max_help_position=35))
        super().__init__(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        arg_type = kwargs.get("type")
        if isinstance(arg_type, type) and issubclass(arg_type, enum.Enum):
            kwargs.setdefault("metavar", "[" + "|".join(e.name for e in arg_type) + "]")

            def parse_enum(s):
                try:
                    return arg_type[s]
                except KeyError:
                    raise argparse.ArgumentTypeError(f"{s!r} is not a valid {arg_type.__name__}")

            kwargs["type"] = parse_enum

        return super().add_argument(*args, **kwargs)

    def _autofix_arguments(self, suggestions, raw_args):
        fixed_args = []
        for arg in raw_args:
            for wrong, right in suggestions:
                if arg == wrong:
                    fixed_args.append(right)
                    break
            else:
                fixed_args.append(arg)
        return fixed_args

    def error(self, message):
        valid_options = []
        for action in self._actions:
            if action.option_strings:
                valid_options.extend(action.option_strings)

        input_options = [arg for arg in sys.argv[1:] if arg.startswith('-')]

        suggestions = []
        for input_opt in input_options:
            matches = difflib.get_close_matches(input_opt, valid_options, n=3, cutoff=0.4)
            if matches:
                suggestions.append((input_opt, matches[0]))

        if suggestions:
            if '--autofix' in sys.argv:
                print(f"{CYAN}Auto-fix enabled. Correcting and re-parsing...{RESET}")
                fixed_args = self._autofix_arguments(suggestions, sys.argv[1:])
                sys.argv = [sys.argv[0]] + fixed_args
                self.parse_args()
                return

            print(f"\n{YELLOW}Error: Unknown or invalid argument(s).{RESET}")
            for wrong, suggestion in suggestions:
                print(f"  Did you mean: {RED}{wrong}{RESET} → {BOLD}{GREEN}{suggestion}{RESET}?")
            print("\nFull message:")
            print(message)
            self.exit(2)
        else:
            self.exit(2, f"{self.prog}: error: {message}\n")

    def format_help(self):
        help_text = super().format_help()
        help_text = help_text.replace("optional arguments:", f"{CYAN}Optional arguments:{RESET}")
        help_text = help_text.replace("options:", f"{CYAN}Optional arguments:{RESET}")
        help_text = help_text.replace("positional arguments:", f"{CYAN}Positional arguments:{RESET}")
        return help_text


# Example usage
if __name__ == "__main__":
    class Mode(enum.Enum):
        FAST = "FAST"
        SLOW = "SLOW"
        MEDIUM = "MEDIUM"

    parser = SnapArgumentParser(description="Demo script with snaparg features.")
    parser.add_argument("--mode", type=Mode, help="Choose a processing mode.")
    parser.add_argument("--count", type=int, help="Number of things to process.")
    parser.add_argument("--autofix", action="store_true", help="Automatically fix mistyped arguments.")
    args = parser.parse_args()
