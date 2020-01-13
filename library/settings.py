class Settings:
    """Values that persist throughout the game."""

    def __init__(self):
        self.screen_width = 1000
        self.screen_height = 672
        self.scroll_rate = -4
        self.bg_scroll_rate = -0.2  # Should always be less than scroll_rate
        self.gravity = 1.2
        self.level_over = False
