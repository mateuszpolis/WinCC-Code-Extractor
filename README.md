# Code Extractor

A Python-based tool for extracting and managing scripts from XML files. This tool is designed to help you:
- Extract scripts from XML files into easily editable CTL files
- Update XML files with modified scripts from CTL files
- Handle scripts both inside and outside of shapes
- Process single files or entire directories recursively

## Features

- **XML to CTL Extraction**:
  - Extracts all scripts from XML files
  - Preserves script context (whether it's inside a shape or not)
  - Creates clearly marked script sections in CTL files
  - Handles XML entities and CDATA sections

- **CTL to XML Updates**:
  - Updates XML files with modified scripts from CTL files
  - Maintains script context (shape association)
  - Properly escapes special characters
  - Wraps content in CDATA sections

- **Directory Processing**:
  - Recursively process all XML or CTL files in a directory
  - Maintains directory structure
  - Provides detailed success/failure statistics

- **Script Context Preservation**:
  - Distinguishes between scripts in shapes and outside shapes
  - Uses `shape_name::script_name` format for scripts inside shapes
  - Prevents accidental script overwrites

## Setup

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/macOS
   # or
   .\venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Usage

### Single File Operations

1. Extract scripts from an XML file:
   ```bash
   python -m src.main extract path/to/file.xml
   ```

2. Update XML from a CTL file:
   ```bash
   python -m src.main update path/to/file.ctl
   ```

### Directory Operations

1. Extract scripts from all XML files in a directory:
   ```bash
   python -m src.main extract-dir path/to/xml/directory
   ```

2. Update all XML files from CTL files in a directory:
   ```bash
   python -m src.main update-dir path/to/ctl/directory
   ```

### File Organization

The tool expects the following directory structure:
- XML files in `/xml/path/to/file.xml`
- CTL files in `/ctl/path/to/file.ctl`

When extracting scripts:
- If input is `/path/to/xml/file.xml`, output will be `/path/to/ctl/file.ctl`
- If input is `xml/file.xml`, output will be `ctl/file.ctl`

### CTL File Format

The CTL files use a clear marker format:

For scripts outside shapes:
```
//START_SCRIPT: script_name
script_content
//END_SCRIPT: script_name
```

For scripts inside shapes:
```
//START_SCRIPT: shape_name::script_name
script_content
//END_SCRIPT: shape_name::script_name
```

## Development

This project uses pre-commit hooks to maintain code quality. The following checks are performed:
- Black (code formatting)
- Flake8 (code linting)
- isort (import sorting)
- Trailing whitespace removal
- End of file fixing

## Error Handling

The tool provides detailed error messages for:
- Missing files
- Malformed XML
- Invalid script contexts
- File access issues

When processing directories, the tool will:
- Continue processing even if some files fail
- Provide a summary of successful and failed operations
- Show detailed error messages for failed files

## License

MIT
