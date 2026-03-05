"""Library management utilities."""

import titlecase


def clean_name(name: str) -> str:
    """Clean a string by capitalizing and removing extra spaces.

    Args:
        name: the name to be cleaned

    Returns:
        str: the cleaned name
    """
    name = " ".join(name.lower().strip().split())
    return str(titlecase.titlecase(name))
