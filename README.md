![GitHub commit activity](https://img.shields.io/github/commit-activity/w/ArchooD2/snaparg) ![GitHub contributors](https://img.shields.io/github/contributors-anon/ArchooD2/snaparg) ![GitHub last commit](https://img.shields.io/github/last-commit/ArchooD2/snaparg) ![PyPI - License](https://img.shields.io/pypi/l/snaparg) ![PyPI - Downloads](https://img.shields.io/pypi/dd/snaparg)
---
# snaparg – Smarter argparse for easy living

`snaparg` is a lightweight Python library that wraps around the built-in `argparse` module, making command-line interfaces more user-friendly by detecting typos in argument names and suggesting the closest valid alternatives.

Perfect for scripts and tools that aim to be a little more forgiving to users without sacrificing the power and flexibility of `argparse`.

You can even replace it in any script just by editing your `import` statement!

---

## ✨ Features

- Drop-in replacement for `argparse.ArgumentParser`
- Detects mistyped CLI flags and suggests corrections
- Compatible with existing `argparse`-based code
- Zero dependencies — works out of the box
- Includes Interactive Mode which prompts for missing arguments to prevent immediate script failure and guide users smoothly.

---


## 📦 Quick Start

- [`pip install snaparg`](https://pypi.org/project/snaparg/)

- then replace:
- `from argparse import ArgumentParser` -> `from snaparg import SnapArgumentParser as ArgumentParser`
---

## 🔧 Example

```bash
$ python demo.py --iput file.txt
Error: Unknown or invalid argument(s).
  Did you mean: '--iput' -> '--input'?

Full message:
usage: demo.py [-h] [--input INPUT] [--output OUTPUT] [--force]
```

---

## 📄 License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0).
See the [LICENSE](LICENSE) file for details.
