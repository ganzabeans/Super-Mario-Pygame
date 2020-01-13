from library.collidables.terrain import Terrain


class Stairs(Terrain):
    """Helper class that creates a list of blocks that make up 1 staircase."""

    def __init__(self, settings, screen, data, direction=-1, re_entry=None):
        super().__init__(settings, screen, "resources/images/stair_block.png", (0, 0), re_entry)
        self.blocks = []
        for i in range(data["count"]):
            starting_position = data["starting"][i]  # Top-left corner of tallest block
            for row in range(data["rows"][i]):
                for column in range(row + 1 + data["columns"][i] - data["rows"][i]):
                    position = starting_position[0] + 48 * column * direction, starting_position[1] + 48 * row
                    stair_block = Terrain(settings, screen, "resources/images/stair_block.png", position, re_entry)
                    self.blocks.append(stair_block)
