class Foo:

    count = 0

    def __iter__(self):
        self.count = 0
        return self

    def __next__(self):
        if self.count < 10:
            self.count += 1
            return self.count
        else:
            raise StopIteration


for i in Foo():
    print(i)
