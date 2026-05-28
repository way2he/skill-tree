def score_article(path: str) -> dict:
    """Stub for daily quality sampling.

    >>> result = score_article('demo.md')
    >>> "total" in result
    True
    >>> 0 <= result["total"] <= 100
    True
    """
    return {
        "total": 75,
        "completeness": 22,
        "relevance": 18,
        "timeliness": 16,
        "readability": 12,
        "practicality": 7,
        "path": path,
    }