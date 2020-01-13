from library.collidables.block import Block


class DeadBlock(Block):
    """Does absolutely nothing."""

    def __init__(self, settings, screen, position, level, re_entry):
        super().__init__(settings, screen, "resources/images/block.png", position, level, re_entry)
