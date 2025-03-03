"""Module for writing extracted scripts to .ctl files."""

from pathlib import Path
from typing import Dict, Tuple, Union

# Type alias for script identifiers
# script_name or (shape_name, script_name)
ScriptKey = Union[
    str, Tuple[str, str]
]  # Either script_name or (shape_name, script_name)  # noqa: E501


def get_ctl_path_from_xml(xml_file_path: Path) -> Path:
    """
    Convert XML file path to corresponding CTL file path.

    Args:
        xml_file_path: Path to the XML file.

    Returns:
        Path to the corresponding CTL file.
    """
    # Convert path to string and normalize separators
    path_str = str(xml_file_path).replace("\\", "/")

    # Handle both absolute and relative paths
    if "/xml/" in path_str:
        # Replace /xml/ with /ctl/ in the path
        ctl_path = path_str.replace("/xml/", "/ctl/")
    else:
        # If /xml/ is not in path, assume it's a relative path
        # and try to find 'xml' folder
        ctl_path = path_str.replace("xml/", "ctl/").replace("xml\\", "ctl/")

    # Change extension from .xml to .ctl
    ctl_path = ctl_path.replace(".xml", ".ctl")

    # Ensure the directory exists
    ctl_file = Path(ctl_path)
    ctl_file.parent.mkdir(parents=True, exist_ok=True)

    return ctl_file


def format_script_key(key: ScriptKey) -> str:
    """
    Format a script key for writing to the CTL file.

    Args:
        key: Script name (str) or a tuple of (shape name, script name).

    Returns:
        A formatted string representation of the key.
    """
    if isinstance(key, tuple):
        shape_name, script_name = key
        return f"{shape_name}::{script_name}"
    return str(key)


def create_ctl_file(
    scripts: Dict[ScriptKey, str], xml_file_path: Path
) -> Path:  # noqa: E501
    """
    Create a .ctl file containing all scripts with clear markers.

    Args:
        scripts: Dictionary of script identifiers and their contents.
        xml_file_path: Path to the original
        XML file (used to name the .ctl file).

    Returns:
        Path to the created .ctl file.

    The format of the .ctl file will be:
    For scripts outside shapes:
    //START_SCRIPT: script_name
    script_content
    //END_SCRIPT: script_name

    For scripts inside shapes:
    //START_SCRIPT: shape_name::script_name
    script_content
    //END_SCRIPT: shape_name::script_name
    """
    # Create .ctl file path with same name as XML file but in ctl directory
    ctl_file_path = get_ctl_path_from_xml(xml_file_path)

    with open(ctl_file_path, "w", encoding="utf-8") as f:
        # Write file header
        f.write("// Auto-generated .ctl file from XML scripts\n")
        f.write(f"// Source: {xml_file_path.name}\n")
        # Format header for shape scripts
        fmt1 = "// Format: shape_name::script_name for"
        fmt2 = " scripts inside shapes\n"
        f.write(fmt1 + fmt2)
        f.write("//         script_name for scripts outside shapes\n\n")

        # Write each script with markers
        for script_key, script_content in scripts.items():
            formatted_key = format_script_key(script_key)
            f.write(f"//START_SCRIPT: {formatted_key}\n")
            f.write(f"{script_content}\n")
            f.write(f"//END_SCRIPT: {formatted_key}\n\n")

    return ctl_file_path
