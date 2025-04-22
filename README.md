# snaparg

`snaparg` is a lightweight Python library that wraps around the built-in `argparse` module, making command-line interfaces more user-friendly by detecting typos in argument names and suggesting the closest valid alternatives.

Perfect for scripts and tools that aim to be a little more forgiving to users without sacrificing the power and flexibility of `argparse`.

---

## ✨ Features

- Drop-in replacement for `argparse.ArgumentParser`
- Detects mistyped CLI flags and suggests corrections
- Compatible with existing `argparse`-based code
- Zero dependencies — works out of the box

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

## 📦 Installation

```pip install snaparg```

---

## 📄 License

This project is licensed under the Mozilla Public License 2.0 (MPL-2.0).
See the [LICENSE](LICENSE) file for details.
