import argparse
import sys
import difflib
import enum
import textwrap

# ANSI colors
BOLD = "\033[1m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"


class SnapArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        # Enable raw formatting to preserve color in help output
        kwargs.setdefault("formatter_class", lambda prog: argparse.HelpFormatter(prog, max_help_position=35))
        super().__init__(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        arg_type = kwargs.get("type")
        if isinstance(arg_type, type) and issubclass(arg_type, enum.Enum):
            # Pretty name for help output
            kwargs.setdefault("metavar", "[" + "|".join(e.name for e in arg_type) + "]")
    
            def parse_enum(s):
                try:
                    return arg_type[s]  # ← name lookup only
                except KeyError:
                    raise argparse.ArgumentTypeError(f"{s!r} is not a valid {arg_type.__name__}")
    
            kwargs.setdefault("type", parse_enum)
    
        return super().add_argument(*args, **kwargs)


    def error(self, message):
        # Grab all valid options
        valid_options = []
        for action in self._actions:
            if action.option_strings:
                valid_options.extend(action.option_strings)

        # Grab all argv args that look like options (start with -)
        input_options = [arg for arg in sys.argv[1:] if arg.startswith('-')]

        # Check for close matches
        suggestions = []
        for input_opt in input_options:
            matches = difflib.get_close_matches(input_opt, valid_options, n=1, cutoff=0.6)
            if matches:
                suggestions.append((input_opt, matches[0]))

            if suggestions:
                print(f"\n{YELLOW}Error: Unknown or invalid argument(s).{RESET}")
                for wrong, suggestion in suggestions:
                    print(f"  Did you mean: {RED}{wrong}{RESET} → {BOLD}{GREEN}{suggestion}{RESET}?")
                print("\nFull message:")


        super().error(message)

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
    args = parser.parse_args()
