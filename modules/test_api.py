from dishesAPIReader import DishesAPIReader
from dishesContainer import DishesContainer


dish_reader = DishesAPIReader()
dish_reader.load_file('test.json')
print('data loaded')
dishes = dish_reader.extract_dishes()
dish_cont = DishesContainer(dishes)
for dish in dish_cont:
    print(dish._health_labels)
    print(dish._daily_info)
    print(dish._nutrients)
    print('\n\n')
