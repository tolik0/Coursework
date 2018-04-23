from dishesAPIReader import DishesAPIReader


dish_reader = DishesAPIReader()
dish_reader.load_data(q='potato, tomato')
print('data loaded')
dishes = dish_reader.extract_dishes()
print(dishes)
