from library.collidables.block import Block


class ItemBlock(Block):
    """Item pops out when hit by player."""

    def __init__(self, settings, screen, position, level, re_entry, has_item):
        super().__init__(settings, screen, "resources/images/yellow_block.png",
                         position, level, re_entry, has_item)
        self.type = "item_block"
