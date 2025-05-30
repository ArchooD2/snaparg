import sys
from .snaparg import SnapArgumentParser

def interactive_parse(parser: SnapArgumentParser):
    """
    Parses command-line arguments, interactively prompting for any missing required values.
    
    If required arguments are missing from the command line, prompts the user to input them, validates and converts the input as needed, and returns the parsed arguments.
    """
    try:
        return parser.parse_args()
    except SystemExit:
        # Find required args not in sys.argv
        missing_args = [
            action for action in parser._actions
            if action.required and (
                (action.option_strings and f'--{action.dest}' not in sys.argv) or
                (not action.option_strings and action.dest not in sys.argv)
            )
        ]

        for action in missing_args:
            if action.option_strings:
                prompt = f"Enter value for --{action.dest}"
            else:
                prompt = f"Enter value for {action.dest}"
            if action.help:
                prompt += f" ({action.help})"
            prompt += ": "

            while True:
                value = input(prompt)
                try:
                    value = action.type(value) if action.type else value
                    sys.argv.extend([f"--{action.dest}", str(value)])
                    break
                except Exception as e:
                    print(f"Invalid value: {e}")

        return parser.parse_args()
