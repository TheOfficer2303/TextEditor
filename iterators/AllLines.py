class AllLinesIterator:
    def __init__(self, lines: list):
        self.lines = lines
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < len(self.lines):
            value = self.lines[self.current]
            self.current += 1
            return value
        else:
            raise StopIteration
