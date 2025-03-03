"""Main module for the Code Extractor application."""

import argparse
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

from .ctl_writer import create_ctl_file
from .xml_parser import extract_scripts
from .xml_updater import update_xml_file


def process_xml_file(xml_file: Path) -> bool:
    """Process a single XML file.

    Args:
        xml_file: Path to the XML file.

    Returns:
        True if processing was successful, False otherwise.
    """
    try:
        # Skip if it's a directory
        if xml_file.is_dir():
            print(f"Skipping directory: {xml_file}")
            return False

        scripts = extract_scripts(str(xml_file))
        print(f"\nFound {len(scripts)} scripts in {xml_file.name}")

        ctl_file_path = create_ctl_file(scripts, xml_file)
        print(f"Created .ctl file: {ctl_file_path.name}")

        print("Extracted scripts:")
        for name in scripts.keys():
            print(f"- {name}")
        return True

    except (FileNotFoundError, ET.ParseError) as e:
        print(f"Error processing {xml_file}: {e}", file=sys.stderr)
        return False


def process_ctl_file(ctl_file: Path) -> bool:
    """Process a single CTL file.

    Args:
        ctl_file: Path to the CTL file.

    Returns:
        True if processing was successful, False otherwise.
    """
    try:
        xml_file_path, num_updates = update_xml_file(ctl_file)
        print(f"\nUpdated {num_updates} scripts in {xml_file_path.name}")
        return True

    except (FileNotFoundError, ET.ParseError) as e:
        print(f"Error processing {ctl_file}: {e}", file=sys.stderr)
        return False


def find_xml_files(directory: Path) -> List[Path]:
    """Find all XML files in the directory and its subdirectories."""
    return list(directory.rglob("*.xml"))


def find_ctl_files(directory: Path) -> List[Path]:
    """Find all CTL files in the directory and its subdirectories."""
    return list(directory.rglob("*.ctl"))


def extract_command(args: argparse.Namespace) -> None:
    """Handle the extract command."""
    process_xml_file(args.xml_file)


def update_command(args: argparse.Namespace) -> None:
    """Handle the update command."""
    process_ctl_file(args.ctl_file)


def extract_dir_command(args: argparse.Namespace) -> None:
    """Handle the extract-dir command."""
    xml_files = find_xml_files(args.directory)

    if not xml_files:
        print(f"No XML files found in {args.directory}")
        return

    print(f"Found {len(xml_files)} XML files to process")

    successful = 0
    failed = 0

    for xml_file in xml_files:
        print(f"\nProcessing {xml_file}")
        if process_xml_file(xml_file):
            successful += 1
        else:
            failed += 1

    print("\nSummary:")
    print(f"- Successfully processed: {successful} files")
    print(f"- Failed to process: {failed} files")
    print(f"- Total files: {len(xml_files)} files")


def update_dir_command(args: argparse.Namespace) -> None:
    """Handle the update-dir command."""
    ctl_files = find_ctl_files(args.directory)

    if not ctl_files:
        print(f"No CTL files found in {args.directory}")
        return

    print(f"Found {len(ctl_files)} CTL files to process")

    successful = 0
    failed = 0

    for ctl_file in ctl_files:
        print(f"\nProcessing {ctl_file}")
        if process_ctl_file(ctl_file):
            successful += 1
        else:
            failed += 1

    print("\nSummary:")
    print(f"- Successfully processed: {successful} files")
    print(f"- Failed to process: {failed} files")
    print(f"- Total files: {len(ctl_files)} files")


def main() -> None:
    """Execute the main program logic."""
    desc = "Extract scripts from XML files"
    desc += " or update them from CTL"
    parser = argparse.ArgumentParser(description=desc)

    subparsers = parser.add_subparsers(
        dest="command", help="Command to execute"
    )  # noqa: E501

    # Extract single file command
    extract_parser = subparsers.add_parser(
        "extract", help="Extract scripts from XML to CTL"
    )
    extract_parser.add_argument("xml_file", type=Path, help="XML file path")

    # Update single file command
    update_parser = subparsers.add_parser(
        "update", help="Update XML with scripts from CTL"
    )
    update_parser.add_argument("ctl_file", type=Path, help="CTL file path")

    # Extract directory command
    extract_dir_parser = subparsers.add_parser(
        "extract-dir", help="Extract scripts from XML files in directory"
    )
    extract_dir_parser.add_argument(
        "directory", type=Path, help="Directory with XML files"
    )

    # Update directory command
    update_dir_parser = subparsers.add_parser(
        "update-dir", help="Update XML files from CTL files in directory"
    )
    update_dir_parser.add_argument(
        "directory", type=Path, help="Directory with CTL files"
    )

    args = parser.parse_args()

    if args.command == "extract":
        extract_command(args)
    elif args.command == "update":
        update_command(args)
    elif args.command == "extract-dir":
        extract_dir_command(args)
    elif args.command == "update-dir":
        update_dir_command(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
