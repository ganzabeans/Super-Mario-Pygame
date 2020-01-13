from pygame import time


class Timer:
    """Helper class that provides images at any given time."""

    def __init__(self, frames, wait=100, index=0, step=1, loop_once=False):
        self.frames = frames
        self.wait = wait
        self.index = index
        self.step = step
        self.loop_once = loop_once
        self.finished = False
        self.last_frame = len(frames) - 1 if step == 1 else 0
        self.last = None

    def _get_index(self):
        now = time.get_ticks()
        if self.last is None:
            self.last = now
            self.index = 0 if self.step == 1 else len(self.frames) - 1
            return 0
        elif not self.finished and now - self.last > self.wait:
            self.index += self.step
            if self.loop_once and self.index == self.last_frame:
                self.finished = True
            else:
                self.index %= len(self.frames)
            self.last = now
        return self.index

    def reset(self):
        self.last = None
        self.finished = False

    def get_image(self, reverse=False):
        if reverse:
            return self.frames[len(self.frames) - self._get_index() - 1]
        else:
            return self.frames[self._get_index()]
