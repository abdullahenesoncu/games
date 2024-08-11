def XY2POS(x, y):
    """Convert board coordinates (x, y) to board position string."""
    return f'{chr(ord("a") + x)}{y + 1}'

def POS2XY(pos):
    """Convert board position string to coordinates (x, y)."""
    return ord(pos[0].lower()) - ord('a'), int(pos[1]) - 1
