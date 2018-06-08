from dish import Dish


class DishesContainer:
    '''Data structure that holds different dishes and gives
    tool to manage them'''
    def __init__(self, dishes):
        self._dishes = dishes
        i = 0
        while i < len(self._dishes):
            try:
                self._dishes[i]
                i += 1
            except ValueError:
                break
        self._size = i

    def __iter__(self):
        return _DishesContainerIterator(self._dishes, self._size)

    def filter_by_health(self):
        pass

    def filter_by_diet(self):
        pass


class _DishesContainerIterator:
    '''Iterator for DishesContainer objects'''
    def __init__(self, dishes, size):
        self._dishes = dishes
        self._current = 0
        self._size = size

    def __iter__(self):
        return self

    def __next__(self):
        if self._current < self._size:
            item = self._dishes[self._current]
            self._current += 1
            return item
        else:
            raise StopIteration
