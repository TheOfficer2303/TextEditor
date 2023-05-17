class RangeIterator:
    def __init__(self, lines, start, stop):
        self.lines = lines
        self.start = start
        self.stop = stop
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.stop:
            value = self.lines[self.current]
            self.current += 1
            return value
        else:
            raise StopIteration
