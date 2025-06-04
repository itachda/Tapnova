def get_required_clicks_for_level(level: int) -> int:
    """
    Returns the number of clicks required to complete a given level.
    Level 1 starts at 3000 and doubles each time.
    """
    base_clicks = 3000
    return base_clicks * (2 ** (level - 1))
