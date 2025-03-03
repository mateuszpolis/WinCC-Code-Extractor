# Code Extractor

A tool for extracting and managing scripts from XML files. This tool allows you to extract scripts from XML files into separate CTL files and update XML files with scripts from CTL files.

## Features

- Extract scripts from single XML files or entire directories
- Update XML files with scripts from CTL files
- Support for scripts both inside and outside shapes
- Automatic CTL file generation with proper formatting
- Directory-based batch processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CodeExtractor.git
cd CodeExtractor
```

2. Set up Git hooks:
```bash
mkdir -p .git/hooks
cp .github/hooks/* .git/hooks/
chmod +x .git/hooks/*
git config commit.template .github/commit-template.txt
```

## Development Conventions

### Branch Naming

All branches must follow this naming convention:
- `feature/description-in-kebab-case` - for new features
- `bugfix/description-in-kebab-case` - for bug fixes
- `hotfix/description-in-kebab-case` - for urgent fixes
- `release/version-number` - for release branches
- `docs/description-in-kebab-case` - for documentation updates

Example: `feature/add-script-extraction`

### Commit Messages

Commit messages must follow this format:
```
<type>: <subject>

<body>
```

Types:
- `feat`: new feature
- `fix`: bug fix
- `refactor`: code refactoring
- `style`: formatting changes
- `docs`: documentation changes
- `test`: test-related changes
- `chore`: build/tool updates

Example:
```
feat: add script extraction functionality

Implement XML script extraction with support for both single files
and directories. Add CTL file generation with proper formatting.
```

## Usage

```bash
# Extract scripts from a single XML file
python -m src.main extract path/to/file.xml

# Update XML file from CTL file
python -m src.main update path/to/file.ctl

# Process all XML files in a directory
python -m src.main extract-dir path/to/directory

# Update all XML files from CTL files in a directory
python -m src.main update-dir path/to/directory
```

## License

[Add your license here]
