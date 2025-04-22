import argparse
import sys
import difflib

class SnapArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
            print("\nError: Unknown or invalid argument(s).")
            for wrong, suggestion in suggestions:
                print(f"  Did you mean: '{wrong}' -> '{suggestion}'?")
            print("\nFull message:")
        
        super().error(message)
