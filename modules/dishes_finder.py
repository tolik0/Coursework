from dishesAPIReader import DishesAPIReader
from dishesContainer import DishesContainer


def find_dishes(ingredients):
    dish_reader = DishesAPIReader()
    dish_reader.load_data(q='+'.join(ingredients))
    print('data loaded')
    dishes = dish_reader.extract_dishes()
    dish_cont = DishesContainer(dishes)
    return dish_cont
