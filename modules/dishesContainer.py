from dish import Dish


class DishesContainer:
    '''Data structure that holds different dishes and gives
    tool to manage them'''
    def __init__(self, dishes):
        if not all(isinstance(x, Dish) for x in dishes):
            raise ValueError('All objects inside dishes-list must be '
                             'of type Dish ')
        self._dishes = dishes

    def __iter__(self):
        return _DishesContainerIterator(self._dishes)

    def filter_by_health(self):
        pass

    def filter_by_diet(self):
        pass


class _DishesContainerIterator:
    '''Iterator for DishesContainer objects'''
    def __init__(self, dishes):
        self._dishes = dishes
        self._current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current < len(self._dishes):
            item = self._dishes[self._current]
            self._current += 1
            return item
        else:
            raise StopIteration
