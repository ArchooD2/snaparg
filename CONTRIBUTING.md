
# Contributing to snaparg

Thank you for your interest in contributing to snaparg! Whether you're reporting bugs, suggesting features, improving documentation, or submitting code, your help is appreciated.

## Getting Started

1. **Fork the Repository**  
   Click the "Fork" button on the top right of the [repository page](https://github.com/ArchooD2/snaparg) to create your own copy.

2. **Clone Your Fork**  
   ```bash
   git clone https://github.com/<your-username>/snaparg.git
   cd snaparg
   ```

3. **Set Up the Environment**  
   It's recommended to use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   pip install -e .[dev]
   ```

## Submitting Changes

1. **Create a Branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make Your Changes**

3. **Add Tests**  
   Add or update tests under the `tests/` directory to cover your changes.

4. **Run Tests**  
   Use `pytest` to ensure everything works:
   ```bash
   pytest
   ```
   (We use `pytest` because it’s lightweight and familiar to most Python devs.)

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add new feature: my-feature"
   git push origin feature/my-feature
   ```

6. **Open a Pull Request**  
   Go to your fork on GitHub and click "Compare & pull request".

## Coding Standards

- Follow [PEP8](https://pep8.org/) style guidelines. (`pip install black` and `black .` are your friends.)
- Include clear docstrings for new functions or classes.
- Use descriptive commit messages.

## Reporting Issues

If you find a bug or have a feature request, please open an [issue](https://github.com/ArchooD2/snaparg/issues) and include as much detail as possible.

## License

By contributing, you agree that your contributions will be licensed under the same license as this project (see `LICENSE`).
