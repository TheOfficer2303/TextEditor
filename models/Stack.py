class Stack(object):
    def __init__(self, attribute_name: str):
        setattr(self, attribute_name, [])
        self.items = getattr(self, attribute_name)

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        else:
            return

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        else:
            return

    def size(self):
        return len(self.items)

    def clear(self):
        self.items = []
