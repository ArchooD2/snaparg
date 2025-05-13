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
# End of ANSI colors

class SnapArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        """
        Initializes the SnapArgumentParser with enhanced defaults.
        
        Sets a custom help formatter with increased help position width and, for Python 3.12+, enables exit on error by default.
        """
        if sys.version_info > (3, 11):
            kwargs.setdefault("exit_on_error", True)
        kwargs.setdefault(
            "formatter_class", partial(argparse.HelpFormatter, max_help_position=35)
        )
        super().__init__(*args, **kwargs)

    def add_argument(self, *args, **kwargs):
        """
        Adds a command-line argument, with enhanced support for enum types.
        
        If the argument type is an enum.Enum subclass, sets the metavar to display valid enum member names and ensures input values are parsed as enum members, raising an error for invalid values.
        """
        arg_type = kwargs.get("type")
        if isinstance(arg_type, type) and issubclass(arg_type, enum.Enum):
            kwargs.setdefault("metavar", "[" + "|".join(e.name for e in arg_type) + "]")

            def parse_enum(s):
                try:
                    return arg_type[s]
                except KeyError:
                    raise argparse.ArgumentTypeError(
                        f"{s!r} is not a valid {arg_type.__name__}"
                    )

            kwargs["type"] = parse_enum

        return super().add_argument(*args, **kwargs)

    def get_registered_actions(self):
        """
        Returns a list of argument actions that have associated option strings.
        
        Only actions representing options (i.e., those with flags like '--foo') are included.
        """
        return [a for a in self._actions if a.option_strings]


    def _autofix_arguments(self, suggestions, raw_args):
        """
        Replaces mistyped arguments in the input list with their suggested corrections.
        
        Args:
            suggestions: A list of (wrong, right) argument string pairs indicating corrections.
            raw_args: The original list of command-line argument strings.
        
        Returns:
            A new list of arguments with mistyped entries replaced by their suggested corrections.
        """
        fixed_args = []
        for arg in raw_args:
            for wrong, right in suggestions:
                if arg == wrong:
                    fixed_args.append(right)
                    break
            else:
                fixed_args.append(arg)
        return fixed_args

    def parse_args(self, args=None, namespace=None):
        """
        Parses command-line arguments and checks for missing required options.
        
        If any required option arguments are missing after parsing, raises an error listing them.
        """
        parsed_args = super().parse_args(args, namespace)
        # Check for missing required arguments
        missing = []
        for action in self.get_registered_actions():
            if getattr(action, "required", False):
                value = getattr(parsed_args, action.dest, None)
                if value is None:
                    missing.append(action.option_strings[0])
        if missing:
            self.error(f"the following arguments are required: {', '.join(missing)}")
        return parsed_args

    def error(self, message):
        """
        Handles command-line parsing errors with enhanced, colorized messages and suggestions.
        
        If a required argument value is missing, displays the expected type and usage tips. For mistyped flags, suggests corrections or automatically fixes them if '--autofix' is present, then exits the program.
        """
        valid_options = []
        for action in self.get_registered_actions():
            if action.option_strings:
                valid_options.extend(action.option_strings)

        input_options = [arg for arg in sys.argv[1:] if arg.startswith("-")]

        suggestions = []
        for input_opt in input_options:
            matches = difflib.get_close_matches(
                input_opt, valid_options, n=3, cutoff=0.4
            )
            if matches:
                suggestions.append((input_opt, matches[0]))

        # 🟡 Case: Missing a value after a valid argument
        if "expected one argument" in message:
            for action in self.get_registered_actions():
                if action.option_strings:
                    for opt in action.option_strings:
                        if opt in sys.argv:
                            # Type hint (default to str if not set)
                            type_hint = (
                                action.type.__name__
                                if hasattr(action.type, "__name__")
                                else "str"
                            )
                            print(
                                f"\n{YELLOW}Error:{RESET} {opt} expects a value of type {BOLD}{CYAN}{type_hint}{RESET}."
                            )
                            print(f"💡 Try: {opt}=value  or  {opt} value")
                            print(
                                f"\n{BOLD}Tip:{RESET} Run with {GREEN}--help{RESET} for usage examples."
                            )
                            self.exit(2)

        # 🔴 Case: Mistyped flags
        if suggestions:
            if "--autofix" in sys.argv:
                print(f"{CYAN}Auto-fix enabled. Correcting and re-parsing...{RESET}")
                fixed_args = self._autofix_arguments(suggestions, sys.argv[1:])
                sys.argv = [sys.argv[0]] + fixed_args
                self.parse_args()
                return

            for wrong, suggestion in suggestions:
                print(
                    f"  Did you mean: {RED}{wrong}{RESET} → {BOLD}{GREEN}{suggestion}{RESET}?"
                )

                # Default argparse fallback
                print(f"\n{RED}Error:{RESET} {message}")
                print(f"\n{BOLD}Tip:{RESET} Run with {GREEN}--help{RESET} for usage.")
                self.exit(2)

    def format_help(self):
        help_text = super().format_help()
        help_text = help_text.replace(
            "optional arguments:", f"{CYAN}Optional arguments:{RESET}"
        )
        help_text = help_text.replace("options:", f"{CYAN}Optional arguments:{RESET}")
        help_text = help_text.replace(
            "positional arguments:", f"{CYAN}Positional arguments:{RESET}"
        )
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
    parser.add_argument(
        "--autofix", action="store_true", help="Automatically fix mistyped arguments."
    )
    args = parser.parse_args()
