
def loose_str_compare(a: str, b: str) -> bool:
    """Compare two strings loosely, ignoring case and whitespace and punctuation."""
    return ''.join(e for e in a if e.isalnum()).lower() == ''.join(e for e in b if e.isalnum()).lower()
