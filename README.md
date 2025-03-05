# Unity Code Documentation Framework

A framework that automatically parses Unity C# code, Shader code, and other programming languages, generating corresponding Markdown documentation and Mermaid diagrams to enhance code readability and maintainability.

## Features

- **Multi-language Support**:
  - Unity C# code
  - Unity Shader code
  - Python code
  - JavaScript code
  - C++ code

- **Documentation Generation**:
  - Markdown documentation with detailed code structure
  - Mermaid class diagrams showing relationships between classes
  - Mermaid flow diagrams showing method calls (optional)

- **Extensible Design**:
  - Easy to add support for additional programming languages
  - Customizable output formats

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/unity-code-doc.git
   cd unity-code-doc
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Command Line Interface

```
python unity_code_parser/main.py [input] [-o OUTPUT] [-p PATTERNS [PATTERNS ...]] [-r] [--no-markdown] [--no-class-diagram] [--flow-diagram]
```

- `input`: Path to a file or directory to process
- `-o, --output`: Directory to save generated documentation (default: docs)
- `-p, --patterns`: File patterns to match (e.g., *.cs *.shader)
- `-r, --recursive`: Process subdirectories recursively
- `--no-markdown`: Do not generate Markdown documentation
- `--no-class-diagram`: Do not generate class diagrams
- `--flow-diagram`: Generate flow diagrams

### Examples

Process a single file:
```
python unity_code_parser/main.py path/to/your/script.cs
```

Process all C# files in a directory and its subdirectories:
```
python unity_code_parser/main.py path/to/your/project -p *.cs -r
```

Process multiple file types and generate flow diagrams:
```
python unity_code_parser/main.py path/to/your/project -p *.cs *.shader *.py -r --flow-diagram
```

## Project Structure

```
unity_code_parser/
├── parser/
│   ├── base_parser.py       # Parser base class
│   ├── csharp_parser.py     # C# code parser
│   ├── shader_parser.py     # Shader code parser
│   ├── python_parser.py     # Python code parser
│   ├── javascript_parser.py # JavaScript code parser
│   └── cpp_parser.py        # C++ code parser
├── generator/
│   ├── markdown_generator.py  # Markdown generator
│   └── mermaid_generator.py   # Mermaid diagram generator
└── main.py                  # Main program
```

## Adding Support for New Languages

To add support for a new programming language:

1. Create a new parser class in the `parser` directory that inherits from `BaseParser`
2. Implement the required methods to extract code structure
3. Update the `get_parser_for_file` function in `main.py` to handle the new file extension

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
