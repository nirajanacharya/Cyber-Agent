"""Document type mapping utilities."""

from typing import Dict


DOC_TYPE_MAPPING: Dict[str, str] = {
    "cyber_awareness_guide": "awareness",
    "nepal_digital_security_act": "cyber_law",
    "nepal_information_technology_act": "cyber_law"
}


def get_doc_type(filename: str) -> str:
    """
    Get document type from filename.
    
    Args:
        filename: Name of the file (e.g., "cyber_awareness_guide.txt")
    
    Returns:
        Document type: "awareness" or "cyber_law"
    """
    file_key = filename.replace(".txt", "")
    return DOC_TYPE_MAPPING.get(file_key, "awareness")
