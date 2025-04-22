# snaparg

`snaparg` is a Python library that wraps around `argparse` to make CLI tools more user-friendly by forgiving small typos in argument names and offering helpful suggestions.

## Example

```bash
$ python demo.py --iput file.txt
Error: Unknown or invalid argument(s).
  Did you mean: '--iput' -> '--input'?

Full message:
usage: demo.py [-h] [--input INPUT] [--output OUTPUT] [--force]
```

## Installation

```bash
pip install snaparg
```

## License

MPL 2.0 License
