"""Module for extracting and processing script contents from XML files."""

import re
import xml.etree.ElementTree as ET
from typing import Dict, Tuple, Union

# Type alias for script identifiers
ScriptKey = Union[
    str, Tuple[str, str]
]  # Either script_name or (shape_name, script_name)


def unescape_xml_content(content: str) -> str:
    """
    Unescape XML content by replacing XML entities with actual characters.

    Args:
        content: The XML content to unescape.

    Returns:
        The unescaped content with XML entities replaced.
    """
    replacements = {
        "&quot;": '"',
        "&apos;": "'",
        "&lt;": "<",
        "&gt;": ">",
        "&amp;": "&",
    }

    for entity, char in replacements.items():
        content = content.replace(entity, char)
    return content


def clean_script_content(content: str) -> str:
    """
    Clean script content by removing CDATA markers and unescaping XML entities.

    Args:
        content: The raw script content from the XML.

    Returns:
        Cleaned script content.
    """
    # Remove CDATA markers
    content = re.sub(r"<!\[CDATA\[", "", content)
    content = re.sub(r"\]\]>", "", content)

    # Unescape XML entities
    content = unescape_xml_content(content)

    # Remove leading/trailing whitespace while preserving internal formatting
    content = content.strip()

    return content


def extract_scripts(
    xml_file_path: str,
) -> Dict[ScriptKey, str]:
    """
    Extract scripts from an XML file and return them as a dictionary.

    Args:
        xml_file_path: Path to the XML file to process.

    Returns:
        A dictionary where keys are either:
        - script name (str) for scripts outside shapes
        - tuple of (shape name, script name) for scripts inside shapes
        Values are the cleaned script contents.

    Raises:
        FileNotFoundError: If the XML file doesn't exist.
        ET.ParseError: If the XML file is malformed.
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        scripts = {}

        # First, find all scripts that are directly
        # under root or non-shape elements
        for script in root.findall(".//script"):
            # Check if this script is inside a shape
            parent_shape = script.find("../[@Name]")
            if parent_shape is None:
                name = script.get("name", "unnamed_script")
                content = script.text if script.text else ""
                scripts[name] = clean_script_content(content)

        # Then, find all scripts inside shapes
        for shape in root.findall(".//*[@Name]"):
            shape_name = shape.get("Name")
            for script in shape.findall(".//script"):
                script_name = script.get("name", "unnamed_script")
                content = script.text if script.text else ""
                key = (shape_name, script_name)
                scripts[key] = clean_script_content(content)

        return scripts

    except FileNotFoundError:
        raise FileNotFoundError(f"XML file not found: {xml_file_path}")
    except ET.ParseError as e:
        raise ET.ParseError(f"Failed to parse XML file: {e}")
