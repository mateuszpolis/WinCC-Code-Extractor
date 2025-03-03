"""Module for updating XML files with scripts from CTL files."""

import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Tuple, Union

# Type alias for script identifiers
# script_name or (shape_name, script_name)
ScriptKey = Union[str, Tuple[str, str]]  # noqa: E501


def escape_xml_content(content: str) -> str:
    """
    Escape special characters in XML content.

    Args:
        content: The content to escape.

    Returns:
        The escaped content with XML entities.
    """
    replacements = {
        '"': "&quot;",
        "'": "&apos;",
        "<": "&lt;",
        ">": "&gt;",
        "&": "&amp;",
    }

    # Replace & first to avoid double-escaping
    content = content.replace("&", "&amp;")
    for char, entity in replacements.items():
        if char != "&":  # Skip & as it's already done
            content = content.replace(char, entity)
    return content


def parse_script_key(key: str) -> ScriptKey:
    """
    Parse a script key from the CTL file format.

    Args:
        key: The script key string from the CTL file.

    Returns:
        Either a script name (str) or a tuple of (shape name, script name).
    """
    if "::" in key:
        shape_name, script_name = key.split("::", 1)
        return (shape_name, script_name)
    return key


def extract_scripts_from_ctl(ctl_file_path: Path) -> Dict[ScriptKey, str]:
    """
    Extract scripts from a CTL file.

    Args:
        ctl_file_path: Path to the CTL file.

    Returns:
        Dictionary mapping script identifiers to their contents.
    """
    scripts = {}
    current_script = None
    current_content = []

    with open(ctl_file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("//START_SCRIPT: "):
                current_script = line.replace("//START_SCRIPT: ", "").strip()
                current_content = []
            elif line.startswith("//END_SCRIPT: "):
                if current_script:
                    script_key = parse_script_key(current_script)
                    scripts[script_key] = "".join(current_content).rstrip()
                current_script = None
            elif current_script is not None:
                current_content.append(line)

    return scripts


def get_xml_path_from_ctl(ctl_file_path: Path) -> Path:
    """
    Convert CTL file path to corresponding XML file path.

    Args:
        ctl_file_path: Path to the CTL file.

    Returns:
        Path to the corresponding XML file.
    """
    # Convert path to string and normalize separators
    path_str = str(ctl_file_path).replace("\\", "/")

    # Handle both absolute and relative paths
    if "/ctl/" in path_str:
        # Replace /ctl/ with /xml/ in the path
        xml_path = path_str.replace("/ctl/", "/xml/")
    else:
        # If /ctl/ is not in path, assume
        # it's a relative path and try to find 'ctl' folder
        xml_path = path_str.replace("ctl/", "xml/").replace("ctl\\", "xml/")

    # Change extension from .ctl to .xml
    xml_path = xml_path.replace(".ctl", ".xml")

    return Path(xml_path)


def update_xml_file(ctl_file_path: Path) -> Tuple[Path, int]:
    """
    Update XML file with scripts from CTL file.

    Args:
        ctl_file_path: Path to the CTL file.

    Returns:
        Tuple of (xml_file_path, number_of_scripts_updated).

    Raises:
        FileNotFoundError: If either CTL or XML file is not found.
        ET.ParseError: If XML file is malformed.
    """
    # Get corresponding XML file path
    xml_file_path = get_xml_path_from_ctl(ctl_file_path)

    if not xml_file_path.exists():
        error_msg = (
            f"XML file not found: {xml_file_path}\n"
            f"Expected XML file path was derived from CTL path: "
            f"{ctl_file_path}"
        )
        raise FileNotFoundError(error_msg)

    # Extract scripts from CTL
    scripts = extract_scripts_from_ctl(ctl_file_path)

    # Parse XML
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Track number of updates
    updates = 0

    # Update scripts outside shapes
    for script in root.findall(".//script"):
        # Skip scripts inside shapes
        if script.find("../[@Name]") is not None:
            continue

        name = script.get("name")
        if name in scripts:
            content = escape_xml_content(scripts[name])
            script.text = f"<![CDATA[{content}]]>"
            updates += 1

    # Update scripts inside shapes
    for shape in root.findall(".//*[@Name]"):
        shape_name = shape.get("Name")
        for script in shape.findall(".//script"):
            script_name = script.get("name")
            key = (shape_name, script_name)
            if key in scripts:
                content = escape_xml_content(scripts[key])
                script.text = f"<![CDATA[{content}]]>"
                updates += 1

    # Save the updated XML
    tree.write(xml_file_path, encoding="UTF-8", xml_declaration=True)

    return xml_file_path, updates
